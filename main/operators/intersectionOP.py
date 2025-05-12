import numpy as np

class intersectionOP:
    def __init__(self, dataSet1, dataSet2, cond=None):
        self.dataSet1 = dataSet1
        self.dataSet2 = dataSet2
        self.cond = cond
        self.opName = "Intersection"

    def execute(self, LLMclient, chatModel, ctxManager):
        # compute the intersection of two sets
        if self.cond is not None:
            intersect = self.dataSet1 & self.dataSet2
        return intersect, ctxManager