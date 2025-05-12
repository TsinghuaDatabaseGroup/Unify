"""
    input:
        Target: Doc, Entity …
        CountBase: list of Doc   or    Text

    output:
        len(CountBase)      (For Target=="Doc")
"""
import json
from prompts import extract_entity_prompt

class countOP:
    def __init__(self, countBase, target, condition):
        self.target = target
        self.countBase = countBase
        self.condition = condition

        self.opName = "Count"

    def execute(self, LLMclient, chatModel, ctxManager):
        if self.condition == None:
            count_result = len(self.countBase)
            entity = None
        else:
            prompt = extract_entity_prompt(self.condition)
            past_messages = [{"role": "user", "content": prompt}]
            response = chatModel.create_completion(LLMclient, messages=past_messages)
            response_json = json.loads(response)
            if response_json:
                entity = response_json["Entities"]
            if self.target == "Doc":
                count_result = len(self.countBase)
        result = {'count': count_result, 'entity': entity}
        ctxManager.store_result(result,'Count')
        return result, ctxManager





