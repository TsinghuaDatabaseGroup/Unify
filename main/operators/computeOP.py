class computeOP:
    def __init__(self, compute_type, *args):
        self.compute_type = compute_type  # Calculate the type, such as "length" or "ratio"
        if compute_type == "length":
            self.documents = args[0]
        elif compute_type == "ratio":
            self.num1, self.num2 = args
        self.opName = "Compute"

    def execute(self, LLMclient, chatModel, ctxManager):
        if self.compute_type == "length":
            return [len(self.documents[doc]) for doc in self.documents], ctxManager
        elif self.compute_type == "ratio":
            if self.num2 == 0:
                raise ValueError("Division by zero in ratio computation")
            return self.num1 / self.num2, ctxManager
        else:
            raise ValueError(f"Unsupported compute type: {self.compute_type}")
