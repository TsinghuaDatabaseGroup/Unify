import numpy as np

class unionOP:
    def __init__(self, dataSet1, dataSet2, cond=None):
        self.dataSet1 = dataSet1
        self.dataSet2 = dataSet2
        self.cond = cond
        self.opName = "Union"

    def execute(self, LLMclient, chatModel, ctxManager):
        # compute the union of two sets
        if self.cond is not None:
            union = self.dataSet1.union(self.dataSet2)
        return union, ctxManager