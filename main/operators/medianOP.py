import numpy as np

class medianOP:
    def __init__(self, data_list):
        self.data_list = data_list

        self.opName = "Median"

    def execute(self, LLMclient, chatModel, ctxManager):
        if not self.data_list:
            return 0
        return np.median(self.data_list), ctxManager