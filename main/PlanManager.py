from openai import OpenAI
from utils.contextManager import LLMContextManager
from operators.computeOP import computeOP
from semanticParse import semantic_parse, replace_parsed_elements_with_identifiers, BQMatcher
from embed import EmbedModel
import json
import copy
from operators.operatorMap import OP_MAP
import re
from utils.placeholders import *

def update_current_question(current_question, bq, formatted_original_question, client, chatModel, ctxManager):
    """
    Reduce the current_question by replacing the part that matches the IDQuestion with the result of the basic question.

    :param current_question:  The original question reduced by the basic questions up to now.
    :param IDQuestion:        The IDQuestion of the current basic question being used.
    :param result:            The result of the current basic question.
    :param formatted_original_question: The part of the current_question that matches the IDQuestion, formatted to the same structure.
    :return:                  The reduced current_question after applying the result of the basic question.
    """
    # Step 0: Extract from BQ
    IDQuestion = bq['IDQuestion']
    result = bq['Return']

    # Step 1: Create a prompt for the LLM to rewrite the current question
    prompt = f"""
    # Task:
    Your task is to reduce the current question by replacing the part that matches the IDQuestion with the result of the basic question. Ensure the reduced question is grammatically correct and makes sense.

    # Example 1:
    # Current question:
    How many documents satisfy being swimming-related are in running domain?

    # Basic Question:
    Documents satisfy [Condition1]

    # Basic Question Result:
    documents

    # Formatted original question:
    Documents satisfy being swimming-related

    # Reduced question:
    How many documents are in running domain?

    # Example 2:
    # Current question:
    From documents related to 'Running,' 'Cycling,' and 'training,' check if the count of documents satisfying all conditions is greater than 5.

    # Basic Question:
    Documents related to [Entity1]

    # Basic Question Result:
    documents

    # Formatted original question:
    Documents related to Running

    # Reduced question:
    From documents related to 'Cycling,' 'training,' check if the count of documents satisfying all conditions is greater than 5.

    # Example 3:
    # Current question:
    From documents, identify the ball sport with the highest ratio of injury-related to training-related documents.

    # Basic Question:
    Group documents by [Entity1]

    # Basic Question Result:
    dictionary

    # Formatted original question:
    Group documents by ball sport

    # Reduced question:
    From dictionary, identify the ball sport with the highest ratio of injury-related to training-related documents.

    # Now please reduce the current question using the provided information.
    # Current question:
    {current_question}

    # Basic Question:
    {IDQuestion}

    # Basic Question Result:
    {result}

    # Formatted original question:
    {formatted_original_question}
    """

    ctxManager.add_user_message(prompt)
    response = chatModel.create_completion(client, messages=ctxManager.get_messages())

    return response.strip(), ctxManager


def verify_bq_format(result, numbered_question):
    """
    Verify if the result matches the format of the numbered_question.
    """
    # Create a regex pattern from the numbered_question
    pattern = re.sub(r'\[([A-Za-z]+\d+)\]', r'.+', numbered_question)
    return re.fullmatch(pattern, result) is not None


def format_question_as_BQ(original_question, numbered_question, client, chatModel, ctxManager):
    """
    Rewrite the part that needs to be processed by the BQ (corresponds to numbered_question) of the original_question
    to strictly follow the BQ format.
    """
    # Step 1: Identify placeholders in the numbered question
    placeholders = re.findall(r'\[([A-Za-z]+\d+)\]', numbered_question)

    # Step 2: Use the LLM to extract and rewrite the corresponding part of the original question
    prompt = f"""
    # Task:
    Your task is to match the original question to a base question. Extract the part of the original question that matches the base question. Express that part in the same form as the base question so that you can work with it the same way as the base question in the subsequent steps.

    # Example 1:
    # Original question: 
    What is the number of documents that satisfy being related to computer science and are published after 2010?  

    # Basic question: 
    Documents satisfy [Condition1]

    # Output:
    Documents satisfy being related to computer science


    # Example 2:
    # Original question: 
    What is the number of documents that are related to sports and involve athletes?   

    # Basic question: 
    Documents satisfy [Condition1]

    # Output:
    Documents satisfy being related to sports


    # Example 3:
    # Original question: 
    What is the number of documents that are written in English?   

    # Basic question: 
    How many documents are [Condition1]

    # Output:
    How many documents are written in English

    # Example 4:
    # Original question:
    From documents related to 'Running,' 'Cycling,' and 'training,' check if the count of documents satisfying all conditions is greater than 5.

    # Basic question:
    Documents related to [Entity1]

    # Output:
    Documents related to Running

    ## Please note that in the original questions of Example 1, Example 2 and Example 4, there are two or more conditions/entities, but in Basic question, there is only one condition/entity, you should rewrite strictly in accordance with Basic question as the examples, and do not combine multiple conditions/entities.

    Now please extract the part of the original question that matches the basic question and rewrite it in the same form as the basic question as above examples. 
    Please only output the result without any other explanations.

    # Original question: 
    {original_question}

    # Basic question: 
    {numbered_question}

    """
    ctxManager.add_user_message(prompt)
    repeat_cnt = 0
    repeat_limit = 5
    while repeat_cnt < repeat_limit:
        repeat_cnt = repeat_cnt + 1
        print(f"[{repeat_cnt}/{repeat_limit}]   Trying to format question as BQ")

        response = chatModel.create_completion(client, max_tokens = 4000, messages=ctxManager.get_messages()).strip()

        if verify_bq_format(response, numbered_question):
            ctxManager.add_assistant_message(response)
            break
        else:
            continue
    # If the number of attempts reaches the limit, add the result to the context manager
    if repeat_cnt == repeat_limit:
        ctxManager.add_assistant_message(response)



    return response.strip(), ctxManager



class planManager:
    def __init__(self, original_question, plan, client, chatModel, BQ_list, all_file_data, parsed_result, partial_question_list, embedModel, index):
        self.original_question = original_question
        self.current_question = original_question
        self.plan = plan
        self.client = client
        self.chatModel = chatModel
        self.BQ_list = BQ_list
        self.all_file_data = all_file_data
        self.ctxManager = LLMContextManager()
        self.parsed_result = parsed_result
        self.partial_question_list = partial_question_list
        self.embedModel = embedModel
        self.index = index

    def explain_plan(self):
        PROMPT = """
        ## Task:
        You are given a question and a corresponding plan.
        The plan was generated using a list of basic questions.
        Your task is to explain how each operator in the plan contributes to answering the original question. 
        Each operator may be nested within other operators, so your explanation should account for this structure.
        
        ## Output:
        Provide the explanation in the following JSON format for each operator in the plan:
        [
            {{
                "Operator": "<operator>",
                "Explanation": "<detailed explanation of what the operator does in the context of the plan and how it helps answer the original question>"
                "Followup Plan" : "<nested plan>"
            }},
            ...
        ]
        
        ## Input:
        ### The original question:
        {}
        
        ### The plan:
        {}
        
        ### The list of basic questions used:
        {}
        
        ## Instructions:
        For each operator in the plan, provide a clear explanation of its role. If an operator contains nested operators, explain each nested operation and how it relates to the larger operation. Follow the hierarchy of the plan structure.
        
        Please output the explanation for each operator in the following JSON format:
        [
            {{
                "Operator": "<operator>",
                "Explanation": "<detailed explanation of what the operator should do in the context of the plan execution and how it helps answer the original question>"
                "Followup Plan" : <nested plan>
            }},
            ...
        ]
        """

        ASK_EXPLAIN_PROMPT = PROMPT.format(self.original_question, self.plan, self.BQ_list)
        print("@@" * 30)

        self.ctxManager.add_user_message(ASK_EXPLAIN_PROMPT)

        response = self.chatModel.create_completion(self.client, messages=self.ctxManager.get_messages())

        print("Explanation of the plan:")
        print(response)

        return response

    def parse_plan_explanation(self, explanation):
        """

        :param explanation:   The generated explanation for the plan by function `explain_plan`
        :return:    The parsed plan explanation, in the form of `nested list of dictionary`
        """
        try:
            parsed_output = json.loads(explanation)
            print("Parsed output:")
            print(json.dumps(parsed_output, indent=2))
        except json.JSONDecodeError:
            print("Failed to parse LLM response for plan explanation as JSON.")
            parsed_output = None

        return parsed_output

    def postorder_sort_plan(self, plan):
        """
            Perform a postorder traversal of the plan's operators.
            :param plan: The plan with explanations and nested followup plans.
            :return: A list of operators in postorder.
        """

        def postorder_traversal(subplan, result):
            for operator in subplan:
                if 'Followup Plan' in operator and operator['Followup Plan']:
                    postorder_traversal(operator['Followup Plan'], result)
                result.append(operator)

        result = []
        postorder_traversal(plan, result)
        return result

    def execute_with_plan(self):
        """
        Execute the plan using self.BQ_list, self.partial_question_list, and self.original_question.
        """

        # please rewrite the postorder_traversal since I should use  postorder_traversal(bq['IDPlan'], mapping, self.ctxManager)
        def postorder_traversal(subplan, mapping, ctxManager):
            for operator in subplan:
                if 'Followup Plan' in operator and operator['Followup Plan']:
                    ctxManager = postorder_traversal(operator['Followup Plan'], mapping, ctxManager)
                # Execute the current operator
                
                op_instance = self.get_operator_instance(operator, mapping, ctxManager)

                # Map placeholders in the operator's parameters into actual values using the mapping
                for key, value in operator.items():
                    if isinstance(value, str) and value in mapping:
                        print("see ")
                        operator[key] = mapping[value]

                res, ctxManager = op_instance.execute(self.client, self.chatModel, ctxManager)

                # Output the result
                # Do not output result for "Scan" operator
                if operator['Operator'] != "Scan":
                    print(f"The {operator['Operator']} result is [{res}]")
                operator["Result"] = res


            return ctxManager

        for bq, partial_question in zip(self.BQ_list, self.partial_question_list):
            # Map placeholders to original text
            # numbered_question = numbering_placeholders(partial_question)
            numbered_question = numbering_placeholders(bq['Question'])
            assert numbered_question == bq['IDQuestion']

            formatted_original_question, self.ctxManager = format_question_as_BQ(self.current_question, numbered_question, self.client, self.chatModel, self.ctxManager)

            import pdb
            pdb.set_trace()
            mapping = map_placeholders_to_original(numbered_question, formatted_original_question)

            print("See mapping used in BQ for the original question")
            print(mapping)
            print("Numbered  Q:  ", numbered_question)
            print("Original  Q:  ", self.original_question)
            print("Current   Q:  ", self.current_question)
            print("Formatted Q:  ", formatted_original_question)
            print("@"*50)

            # Traverse and execute the subplan in post-order
            self.ctxManager = postorder_traversal(bq['IDPlan'], mapping, self.ctxManager)

            # The following is the update of the global doc set
            print()
            
            if bq['IDPlan'][0]['Operator'] == "Scan":
                scanned_data = bq['IDPlan'][0]['Result']
                print(f"Update the doc set, total docs: [{len(scanned_data)}]")
                scanned_data_ids = []
                def find_from_dict(data_dict, Qvalue):
                    # suppose only one matching
                    for key, value in data_dict.items():
                        if value == Qvalue: 
                            return key
                for key, doc in scanned_data.items():
                    # scanned_data_ids.append(self.all_file_data.find(doc))
                    scanned_data_ids.append(find_from_dict(self.all_file_data, doc))
                # self.all_file_data = {i:self.all_file_data[i] for i in scanned_data_ids}
                if scanned_data_ids:
                    self.all_file_data = {i:self.all_file_data[i] for i in scanned_data_ids}
                else:
                    self.all_file_data = {}
                    print("⚠️ No documents matched the scan condition")
            # Update the current question
            self.current_question, self.ctxManager = update_current_question(self.current_question,
                                                                 bq,
                                                                 formatted_original_question,
                                                            client=self.client,
                                                            chatModel=self.chatModel,
                                                            ctxManager=self.ctxManager)

            print("After update, current question becomes:")
            print(self.current_question)

        # Print the final context manager messages
        print("Final context manager messages:")
        print(self.ctxManager.get_messages())

    def get_operator_instance(self, operator, mapping, ctxManager):
        """
        Get the instance of the operator class based on the operator type.
        :param operator: The operator dictionary containing the type and other details.
        :return: An instance of the operator class.
        """
        operator_type = operator['Operator']
        # Assuming you have a mapping of operator types to their classes
        # operator_class = self.operator_mapping.get(operator_type)
        operator_class = OP_MAP[operator_type]
        print("operator class is ", operator_class)
        if not operator_class:
            raise ValueError(f"Unknown operator type: {operator_type}")


        def replace_variables(input_string, mapping):
            # Find all occurrences of variables surrounded by []
            variables = re.findall(r'\[(.*?)\]', input_string)

            # Replace the variables with their values from the mapping
            for var in variables:
                if var in mapping:
                    input_string = input_string.replace(f'[{var}]', mapping[var])

            return input_string

        def check_follow_format(s):
            # Use a regular expression to match the pattern "follow_i" where i is a number
            match = re.fullmatch(r"follow_(\d+)", s)
            if match:
                return True, int(match.group(1))  # Convert the captured number to an integer
            else:
                return False, None

        # Different operators use different constructor functions

        if operator_type == "Scan":
            if len(operator["Parameter"]) == 1:
                CONDITION = replace_variables(operator["Parameter"][0], mapping)
                data_list = self.all_file_data
            elif len(operator["Parameter"]) == 2:
                CONDITION = replace_variables(operator["Parameter"][0], mapping)
                data_list = operator["Parameter"][1]
                if_follow, follow_id = check_follow_format(data_list)
                if if_follow:
                    data_list = operator['Followup Plan'][follow_id]['Result']
            print("Scan condition is ")
            print(CONDITION)
            return operator_class(CONDITION, data_list, self.client, self.chatModel, self.ctxManager)

        
        elif operator_type == "Count":
            if len(operator["Parameter"]) == 1:
                countTarget = operator["Parameter"][0]
                countBase = self.all_file_data
                condition = None
            else:
                countBase = operator["Parameter"][0]
                if_follow, follow_id = check_follow_format(countBase)
                if if_follow:
                    countBase = operator['Followup Plan'][follow_id]['Result']
                countTarget = operator["Parameter"][1]
                condition = replace_variables(operator["Parameter"][2], mapping)
            return operator_class(countBase, countTarget, condition)
        
        elif operator_type == "Compare":
            cmpTarget = operator["Parameter"][0]
            if cmpTarget in ["max", "min"] and len(operator["Parameter"]) == 2:  # Multi-entity comparison
                entities_values = ctxManager.results[operator["Parameter"][1]].pop()
                if isinstance(entities_values, str) and entities_values.startswith("[["):  # Handle nested lists
                    try:
                        entities_values = eval(replace_variables(entities_values, mapping))  # Convert to Python list
                    except:
                        raise ValueError(f"Invalid entities_values format: {entities_values}")
                if isinstance(entities_values, dict):  # If it's a dictionary, convert to list
                    entities_values = [(entity, value) for entity, value in entities_values.items()]
                return operator_class(cmpTarget, entities_values=entities_values)
            else:
                count_data = ctxManager.results[operator["Parameter"][1]]
                A = count_data.pop()
                Avalue = A.get("count")  # Get count value
                Aname = A.get("entity")  # Get entity name
                B = count_data.pop()
                Bvalue = B.get("count")  # Get count value
                Bname = B.get("entity")  # Get entity name
                return operator_class(cmpTarget, Avalue = Avalue, Bvalue = Bvalue, A = Aname, B = Bname)

        elif operator_type == "Compute":
            compute_type = operator["Parameter"][0]
            if compute_type == "ratio":  # New ratio calculation
                num1 = operator["Parameter"][1]
                if_follow, follow_id = check_follow_format(num1)
                if if_follow:
                    num1 = operator['Followup Plan'][follow_id]['Result']
                num2 = operator["Parameter"][2]
                if_follow, follow_id = check_follow_format(num2)
                if if_follow:
                    num2 = operator['Followup Plan'][follow_id]['Result']
                return operator_class(compute_type, num1, num2)
            else:
                data_list = self.all_file_data
                return operator_class(compute_type, data_list)
        
        elif operator_type == "Average":
            data_list = operator["Parameter"][0]
            if_follow, follow_id = check_follow_format(data_list)
            if if_follow:
                data_list= operator['Followup Plan'][follow_id]['Result']
            else:
                assert False
            return operator_class(data_list)
        elif operator_type == "Max":
            data_list = operator["Parameter"][0]
            if_follow, follow_id = check_follow_format(data_list)
            if if_follow:
                data_list= operator['Followup Plan'][follow_id]['Result']
            else:
                assert False
            return operator_class(data_list)
        elif operator_type == "Min":
            data_list = operator["Parameter"][0]           
            if_follow, follow_id = check_follow_format(data_list)
            if if_follow:
                data_list= operator['Followup Plan'][follow_id]['Result']
            else:
                assert False
            return operator_class(data_list)
        elif operator_type == "Median":
            data_list = operator["Parameter"][0]
            if_follow, follow_id = check_follow_format(data_list)
            if if_follow:
                data_list= operator['Followup Plan'][follow_id]['Result']
            else:
                assert False
            return operator_class(data_list)
        elif operator_type == "Sum":
            data_list = operator["Parameter"][0]
            if_follow, follow_id = check_follow_format(data_list)
            if if_follow:
                data_list= operator['Followup Plan'][follow_id]['Result']
            else:
                assert False
            return operator_class(data_list)
        elif operator_type =="Percentile":
            data_list = operator["Parameter"][0]
            if_follow, follow_id = check_follow_format(data_list)
            if if_follow:
                data_list = operator['Followup Plan'][follow_id]['Result']
            else:
                assert False
            p =  replace_variables(operator["Parameter"][0], mapping)
            p = p/100
            return operator_class(data_list, p)
        elif operator_type =="OrderBy":
            attribute = replace_variables(operator["Parameter"][0], mapping)
            order = replace_variables(operator["Parameter"][1], mapping)
            return operator_class(self.all_file_data, attribute, order)
        
        elif operator_type == "Ratio":
            grouped_data = ctxManager.results[operator["Parameter"][0]]
            condition1 = replace_variables(operator["Parameter"][1], mapping)
            condition2 = replace_variables(operator["Parameter"][2], mapping)
            return operator_class(grouped_data, condition1, condition2)
        
        elif operator_type == "Conditional":
            result = ctxManager.results[operator["Parameter"][0]].pop()
            count_result = result.get("count")
            comparator = replace_variables(operator["Parameter"][1], mapping)
            threshold = replace_variables(operator["Parameter"][2], mapping)
            return operator_class(count_result, comparator, threshold)
        
        elif operator_type =="Extract":
            return operator_class(self.all_file_data)
        elif operator_type =="GroupBy":
            GROUPBYATTR = replace_variables(operator["Parameter"][0], mapping)
            print("Groupby attribute is ")
            print(GROUPBYATTR)
            return operator_class(self.all_file_data, GROUPBYATTR)
        elif operator_type =="Classify":
            ClassifyCond = replace_variables(operator["Parameter"][0], mapping)
            return operator_class(ClassifyCond, self.all_file_data)
        elif operator_type =="TopK":
            K = replace_variables(operator["Parameter"][0], mapping)
            return operator_class(int(K), self.all_file_data)
        elif operator_type =="Join":
            data_0 = replace_variables(operator["Parameter"][0], mapping)
            data_1 = replace_variables(operator["Parameter"][1], mapping)
            att_0 = replace_variables(operator["Parameter"][2], mapping)
            att_1 = replace_variables(operator["Parameter"][3], mapping)
            return operator_class(data_0, data_1, att_0, att_1)
        elif operator_type =="Union":
            data_0 = replace_variables(operator["Parameter"][0], mapping)
            data_1 = replace_variables(operator["Parameter"][1], mapping)
            return operator_class(data_0, data_1)
        elif operator_type =="Intersection":
            data_0 = replace_variables(operator["Parameter"][0], mapping)
            data_1 = replace_variables(operator["Parameter"][1], mapping)
            return operator_class(data_0, data_1)
        elif operator_type =="Complementary":
            data_0 = replace_variables(operator["Parameter"][0], mapping)
            data_1 = replace_variables(operator["Parameter"][1], mapping)
            return operator_class(data_0, data_1)
        elif operator_type:
            return operator_class(operator['Explanation'])
        else:
            raise ValueError(f"Unknown operator type: {operator_type}")