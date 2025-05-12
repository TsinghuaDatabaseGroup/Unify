import numpy as np
from prompts import get_classify_prompt

class classifyOP:
    def __init__(self, cond, data):
        self.data = data
        self.cond = cond
        self.opName = "Classify"


    def execute(self, LLMclient, chatModel, ctxManager):
        # classify data based on cond
        category = self.classify(self.data, self.cond, LLMclient, chatModel, ctxManager)
        return category

    def classify(self, data, cond, LLMclient, chatModel, ctxManager):
        PROMPT = get_classify_prompt(cond, data)
        ctxManager.add_user_message(PROMPT)
        response = chatModel.create_completion(
            LLMclient,
            temperature=0.1,
            top_p=0.9,
            max_tokens=4000,
            messages=ctxManager.get_messages()
        )
        return response.strip()

