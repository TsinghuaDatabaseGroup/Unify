"""
    通过一个prompt完成执行的operator
"""
class retrieveOP:
    def __init__(self, index, embedModel):
        self.index = index
        self.embedModel = embedModel
        self.GET_RETRIEVE_QUERY_PROMPT = """
            Please give me the content you want to use as the query for Retrieve without any other output.
        """

        self.ANSWER_FOR_RETRIEVE = """
            The retrieved results are {}.  
            You can decide for yourself whether the results of retrieve are helpful or not.
        """

        self.opName = "Retrieve"

        # self.prompt = prompt
    def execute(self, LLMclient, chatModel, ctxManager):
        ctxManager.add_user_message(self.GET_RETRIEVE_QUERY_PROMPT)
        self.retgrieveQuery = chatModel.create_completion(
            LLMclient,
            temperature=0.1,
            top_p=0.9,
            max_tokens=100,
            messages=ctxManager.get_messages()
        )
        ctxManager.add_assistant_message(self.retgrieveQuery)
        retrieval_results, result_file_ids, result_chunk_locs = self.index.search(self.retgrieveQuery, self.embedModel)

        ctxManager.add_user_message(self.ANSWER_FOR_RETRIEVE.format(retrieval_results))

        return ctxManager



