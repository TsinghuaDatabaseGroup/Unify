class compareOP:
    def __init__(self, cmpTarget, entities_values=None, Avalue=None, Bvalue=None, A=None, B=None):
        self.cmpTarget = cmpTarget  # "max" 或 "min"
        if entities_values:  # Multi-entity comparison
            self.entities_values = entities_values  # [(entity1, value1), (entity2, value2), ...]
        else:  # Comparison of Two Entities
            self.A, self.B = A, B
            self.Avalue, self.Bvalue = Avalue, Bvalue
        self.opName = "Compare"

    def execute(self, LLMclient, chatModel, ctxManager):
        if hasattr(self, "entities_values"):  # Multi-entity comparison
            if not self.entities_values:
                raise ValueError("No entities provided for comparison")
            values = [pair[1] for pair in self.entities_values]
            entities = [pair[0] for pair in self.entities_values]
            if self.cmpTarget == "max":
                max_idx = values.index(max(values))
                return entities[max_idx], ctxManager
            elif self.cmpTarget == "min":
                min_idx = values.index(min(values))
                return entities[min_idx], ctxManager
            else:
                raise ValueError(f"Unsupported comparison target: {self.cmpTarget}")
        else:  # Comparison of Two Entities
                if self.cmpTarget == "max":
                    # return self.A and self.B that has with max value
                    cmp_result = self.A if self.Avalue > self.Bvalue else self.B
                elif self.cmpTarget == "min":
                    # return self.A and self.B that has with min value
                    cmp_result = self.A if self.Avalue < self.Bvalue else self.B
                return cmp_result, ctxManager




