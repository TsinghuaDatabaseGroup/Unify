from prompts import get_scan_prompt

# ratioOP
class RatioOP:
    def __init__(self, grouped_data, condition1, condition2):
        self.grouped_data = grouped_data.pop()
        self.condition1 = condition1      
        self.condition2 = condition2      
        self.opName = "Ratio"

    def execute(self, LLMclient, chatModel, ctxManager):
        ratios = {}
        for group_key, docs in self.grouped_data.items():
            # Calculate the number of documents that meet condition1
            count1 = sum(1 for doc in docs.values() if self._check_condition(doc, self.condition1, LLMclient, chatModel, ctxManager))
            # Calculate the number of documents that meet condition2
            count2 = sum(1 for doc in docs.values() if self._check_condition(doc, self.condition2, LLMclient, chatModel, ctxManager))
            # ratio
            ratios[group_key] = count1 / count2 if count2 != 0 else 0
        ctxManager.store_result(ratios,'Ratio')
        return ratios, ctxManager
    
    def _check_condition(self, doc, condition, LLMclient, chatModel, ctxManager):
        prompt = get_scan_prompt(condition,doc)
        ctxManager.add_user_message(prompt)
        response = chatModel.create_completion(
            LLMclient,
            temperature=0.1,
            top_p=0.9,
            max_tokens=1000,
            messages=ctxManager.get_messages()
        )
        ctxManager.pop_latest_message()
        return "Yes" in response
