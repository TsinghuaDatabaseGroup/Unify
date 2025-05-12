"""
    Extract the doc that conforms to the query from the list containing all the doc
    Unlike scanOP.py, it uses index to quickly locate and look for Docs similar to top-K
"""
from tqdm import tqdm

class indexScanOP:
    def __init__(self, condition, docSet, embedModel, index, all_file_data):
        self.condition = condition
        self.docSet = docSet
        self.embedModel = embedModel
        self.index = index
        self.all_file_data = all_file_data

        self.opName = "IndexScan"

    def execute(self, LLMclient, chatModel, ctxManager):
        """
        Execute the scan operation to find documents that satisfy the condition.
        :param LLMclient: The LLM client used to evaluate the documents.
        :param ctxManager: The context manager to maintain the LLM context.
        :return: A list of documents that satisfy the condition.
        """

        GENED_PROMPT = f"""Does the document satisfy the condition: "talks about {self.condition}"? """

        print(GENED_PROMPT)


        result_list = []

        RETRIEVE_QUERY = f"{self.condition}"
        print("🦍 Retrieve Query Is")
        print(RETRIEVE_QUERY)

        ######### 【Using index, quickly locate a part, then filter them one by one, and determine whether to continue searching】

        sampleProp = 0.5
        K = int(sampleProp * self.index.docNum)

        retrieval_results, result_file_ids, result_chunk_locs = self.index.search(RETRIEVE_QUERY, self.embedModel, K=K)
        
        check_file_list = result_file_ids

        recentNoNum = 0

        for file_id in tqdm(check_file_list):
            file_content = self.all_file_data[file_id]

            # predicate_prompt = """Here is the query over a document. """ + f""" "{GENED_PROMPT}"\n """ + f"""\n The document has following content:\n"{file_content}"\n
            # Please output 'Yes' if the document satisfies the query, and 'No' otherwise."""

            predicate_prompt = f"""
            Here is the query over a document.

            ## Query: {GENED_PROMPT}
            ## The document:
            {file_content}

            ## Task: Please output 'Yes' if the document satisfies the query, and 'No' otherwise.

            """

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
                result_list.append(file_content)
                recentNoNum = 0
            else:
                recentNoNum = recentNoNum + 1


            ctxManager.pop_latest_message()

            if recentNoNum >=4:
                break
        return result_list, ctxManager





