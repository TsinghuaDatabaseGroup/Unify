import re
class extractOP:
    def __init__(self, data_list, extract_target="Question viewcount"):
        self.data_list = data_list
        if type(self.data_list) == dict:
            self.data_list = list(self.data_list.values())


        self.extract_target = extract_target
        self.extract_target = "Question viewcount"

        self.opName = "Extract"


    def execute(self, LLMclient, chatModel, ctxManager):
        pattern = re.compile(rf"{self.extract_target}: (\d+)")
        extracted_values = []

        for item in self.data_list:
            match = pattern.search(item)
            # extract the value from match
            if match:
                extracted_values.append(int(match.group(1)))

        return extracted_values, ctxManager




