class maxOP:
    def __init__(self, data_list):
        self.data_list = data_list

        self.opName = "Max"

    def execute(self, LLMclient, chatModel, ctxManager):
        if not self.data_list:
            return 0
        return max(self.data_list), ctxManager
