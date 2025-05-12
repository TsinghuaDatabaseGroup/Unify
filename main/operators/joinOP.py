import numpy as np

class joinOP:
    def __init__(self, dataSet1, dataSet2, joinAtt1, joinAtt2, cond=None):
        self.dataSet1 = dataSet1
        self.dataSet2 = dataSet2
        self.joinAtt1 = joinAtt1
        self.joinAtt2 = joinAtt2
        self.opName = "Join"

    def execute(self, LLMclient, chatModel, ctxManager):
        # join dataSet1 and dataSet2 on joinAtt1 == joinAtt2
        joinResult = self.join(self.dataSet1, self.dataSet2, self.joinAtt1, self.joinAtt2)
        return joinResult, ctxManager

    def join(self, dataSet1, dataSet2, joinAtt1, joinAtt2):
        joinResult = []
        for item1 in dataSet1:
            for item2 in dataSet2:
                if item1[joinAtt1] == item2[joinAtt2]:
                    joinResult.append({**item1, **item2})
        return joinResult