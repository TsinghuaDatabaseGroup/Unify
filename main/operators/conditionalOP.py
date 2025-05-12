# conditionalOP
class ConditionalOP:
    def __init__(self, count_result, operator, threshold):
        self.count_result = count_result
        self.operator = operator  # ">", "<", "=="
        self.threshold = int(threshold)
        self.opName = "Conditional"

    def execute(self, LLMclient, chatModel, ctxManager):
        if self.operator == ">":
            result = "Yes" if self.count_result > self.threshold else "No"
        elif self.operator == "<":
            result = "Yes" if self.count_result < self.threshold else "No"
        elif self.operator == "==":
            result = "Yes" if self.count_result == self.threshold else "No"
        else:
            result = "Invalid operator"
        return result, ctxManager