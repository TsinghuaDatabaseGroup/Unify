from numba.tests.test_dispatcher import dummy
from tqdm import tqdm
from prompts.operators.scan import *
from prompts.operators.extract import *

from prompts import get_scan_prompt, get_check_if_semantic_prompt, get_op_literals
from utils.contextManager import LLMContextManager
import numpy as np
import re

class scanOP:
    def __init__(self, condition, docSet, client, chatmodel, ctxManager):
        self.condition = condition
        self.docSet = docSet
        self.docList = list(self.docSet.values())
        self.docKeyList = list(self.docSet.keys())
        self.chatmodel = chatmodel
        self.client = client
        self.ctxManager = ctxManager
        self.opName = "Scan"
        self.extract_op = None
        self.extract_literal = None
        

        self.useSemantic = self.if_use_semantic()
        print("🦍 useSemantic: ", self.useSemantic)
        if self.useSemantic:
            self.execute = self.execute_with_semantic
        else:
            if "explicit" in self.condition:
                print("Use keyword for scan")
                self.execute = self.execute_without_semantic
            else:
                print("Use regex for scan")

                self.extract_target = self._parse_target_field(condition)
                print(f"🔍 Extracted target field: {self.extract_target}")
                self.extract_op, self.extract_literal = self.extract_op_literals(self.condition)
                operator_mapping = {
                    "is greater than": '>',
                    "greater than": '>',
                    "larger than": '>',
                    "exceeds": '>',
                    "is less than": '<',
                    "less than": '<',
                    "below": '<',
                    "equals": '=',
                    "equal to": '=',
                }
                self.extract_op = operator_mapping.get(self.extract_op.lower(), self.extract_op)
                print(f"Extracted Operator: {self.extract_op}, Literal: {self.extract_literal}")

                self.execute = self.execute_without_semantic_regex

    def if_use_semantic(self):
        # check if the condition needs semantic understanding
        if_semantic_PROMPT = get_check_if_semantic_prompt(self.condition)
        self.ctxManager.add_user_message(if_semantic_PROMPT)
        response = self.chatmodel.create_completion(self.client, max_tokens = 4000, messages=self.ctxManager.get_messages())
        return "Yes" in response

    def _parse_target_field(self, condition):
        """Parse the target field from the conditions. Example: 'views > 10000' -> 'views'"""
        match = re.search(
            r"(\b[a-zA-Z]+\b)\s*(?:larger than|greater than|less than|>|<|=)", 
            condition, 
            re.IGNORECASE
        )
        base_field = match.group(1).lower() if match else "views"  # default
        # Extended field mapping table
        field_mapping = {
            "views": ["Question viewcount"],
            "picks": ["draft picks", "total picks"]
        }
        
        # Search for the best matching field
        for doc in self.docList[:5]:  # Sample and inspect the first 5 documents
            for candidate in field_mapping.get(base_field, [base_field]):
                if re.search(rf"{candidate}:\s*\d+", doc, re.IGNORECASE):
                    return candidate
        return base_field

    def extract_op_literals(self, condition):
        PROMPT = get_op_literals(condition)
        self.ctxManager.add_user_message(PROMPT)
        response = self.chatmodel.create_completion(self.client, max_tokens = 4000, messages=self.ctxManager.get_messages())
        operator = response.split(",")[0].strip()
        literal = int(response.split(",")[1].strip())
        return operator, literal

    def execute_without_semantic(self, LLMclient, chatModel, ctxManager):
        self.ctxManager.add_user_message(get_keyword_prompt(self.condition))
        keyword = self.chatmodel.create_completion(self.client, max_tokens = 4000, messages=self.ctxManager.get_messages())
        print(f"extracted keyword:  [{keyword}]")

        result_dict = {}
        for file_name, file_content in self.docSet.items():
            if keyword in file_content:
                result_dict[file_name] = file_content
        return result_dict, ctxManager

    def execute_without_semantic_regex(self, LLMclient, chatModel, ctxManager):
        # If there are operators and literals, use numerical comparison
        if self.extract_op and self.extract_literal is not None:
            target_pattern = re.escape(self.extract_target).replace(r"\ ", r"\s+")
            pattern = re.compile(rf"{target_pattern}:\s*(\d+)", re.IGNORECASE)
        else:
            # If there are no operators and literals, use keyword matching
            pattern = re.compile(rf"{re.escape(self.extract_op)}", re.IGNORECASE)
        
        extracted_values = []
        matched_docs = []
        for idx, item in enumerate(self.docList):
            match = pattern.search(item)
            if match:
                if self.extract_literal is not None:
                    try:
                        extracted_value = int(match.group(1))
                        extracted_values.append(extracted_value)
                        matched_docs.append(idx)
                        # print(f"Matched Document {self.docKeyList[idx]}: {extracted_value}")
                    except ValueError:
                        print(f"Failed to convert extracted value to int in document {self.docKeyList[idx]}")
                else:
                    extracted_values.append(item)
                    matched_docs.append(idx)
                    # print(f"Matched Document {self.docKeyList[idx]}: {item}")

        if self.extract_op and self.extract_literal is not None:
            if self.extract_op == '>':
                indices = [i for i, val in enumerate(extracted_values) if val > self.extract_literal]
            elif self.extract_op == '=':
                indices = [i for i, val in enumerate(extracted_values) if val == self.extract_literal]
            elif self.extract_op == '<':
                indices = [i for i, val in enumerate(extracted_values) if val < self.extract_literal]
            else:
                print(f"Unsupported operator: {self.extract_op}")
                indices = []
        else:
            indices = [i for i, val in enumerate(extracted_values) if val]

        result_list = {self.docKeyList[matched_docs[i]]: self.docList[matched_docs[i]] for i in indices}

        return result_list, ctxManager


    def execute_with_semantic(self, LLMclient, chatModel, ctxManager):
        """
        Execute the scan operation to find documents that satisfy the condition.
        :param LLMclient: The LLM client used to evaluate the documents.
        :param ctxManager: The context manager to maintain the LLM context.
        :return: A list of documents that satisfy the condition.
        """
        result_dict = {}

        for file_name, file_content in tqdm(self.docSet.items()):
            predicate_prompt = get_scan_prompt(self.condition, file_content)

            ctxManager.add_user_message(predicate_prompt)
            
            exec_result = chatModel.create_completion(
                LLMclient,
                temperature=0.1,
                top_p=0.9,
                max_tokens=100,
                messages=ctxManager.get_messages()
            )

            print("--- see exec result")
            print(exec_result)

            if "Yes" in exec_result:
                
                result_dict[file_name] = file_content

            ctxManager.pop_latest_message()

        return result_dict, ctxManager





