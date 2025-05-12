import numpy as np

class complementaryOP:
    def __init__(self, dataSet1, dataSet2, cond=None):
        self.dataSet1 = dataSet1
        self.dataSet2 = dataSet2

        self.opName = "Complementary"
        self.cond = cond

    def execute(self, LLMclient, chatModel, ctxManager):
        # compute the intersection of two sets
        if self.cond is not None:
            complement = self.dataSet1 - self.dataSet2
        return complement, ctxManager