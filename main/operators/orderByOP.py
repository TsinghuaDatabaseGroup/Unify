import numpy as np

class orderByOP:
    def __init__(self, data_list, attribute, order="ascending"):
        self.data_list = data_list
        self.attribute = attribute
        self.order = order
        self.opName = "OrderBy"

    def execute(self, LLMclient, chatModel, ctxManager):
        if not self.data_list:
            return [], ctxManager
        reverse = True if self.order.lower() == "descending" else False
        try:
            sorted_data = sorted(self.data_list, key=lambda x: x[self.attribute], reverse=reverse)
        except KeyError:
            sorted_data = self.data_list  # Fallback if attribute not found
        return sorted_data, ctxManager