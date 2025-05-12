import re
import numpy as np
from prompts import get_attribute_prompt

class groupByOP:
    def __init__(self, dataSet, groupByAttribute):
        self.dataSet = dataSet
        if type(self.dataSet) == dict:
            self.data_list = list(self.dataSet.values())
            self.dataKey_list = list(self.dataSet.keys())
        else:
            self.data_list = self.dataSet
            self.dataKey_list = np.arange(len(self.data_list))
        self.groupByAttribute = groupByAttribute
        self.opName = "GroupBy"

    def execute(self, LLMclient, chatModel, ctxManager):
        extracted_values = [self.extractAttr(LLMclient, chatModel, item) for item in self.data_list]
        grouped_data = {}
        for i, value in enumerate(extracted_values):
            if value not in grouped_data:
                grouped_data[value] = {}
            grouped_data[value][self.dataKey_list[i]] = self.data_list[i]
        ctxManager.store_result(grouped_data,'GroupBy')
        return grouped_data, ctxManager
    
    def extractAttr(self, LLMclient, chatModel, item):       
        PROMPT = get_attribute_prompt(self.groupByAttribute, item)
        response = chatModel.create_completion(LLMclient, messages=[{"role": "user", "content": PROMPT}])
        return response if response != "Unknown" else "Unknown"
