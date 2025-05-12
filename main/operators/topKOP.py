import numpy as np

class topKOP:
    def __init__(self, K, data_list):
        self.data_list = data_list
        self.K = K
        self.opName = "TopK"

    def execute(self, LLMclient, chatModel, ctxManager):
        if not self.data_list:
            return 0
        # return top K elements in self.data_list
        sorted_data = sorted(self.data_list, reverse=True)
        return sorted_data[:self.K], ctxManager