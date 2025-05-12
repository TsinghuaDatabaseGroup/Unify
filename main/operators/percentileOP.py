import numpy as np

class percentileOP:
    def __init__(self, data_list, p):
        self.data_list = data_list
        self.p = p
        self.opName = "Percentile"

    def execute(self, LLMclient, chatModel, ctxManager):
        if not self.data_list:
            return 0
        return np.percentile(self.data_list, self.p), ctxManager