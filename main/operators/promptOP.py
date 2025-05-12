from .genPromptOP import genPromptOP

class promptOP:
    def __init__(self, prompt):
        self.prompt = prompt
        self.opName = "Prompt"

    def execute(self, LLMclient, chatModel, ctxManager, useGenPrompt=False):
        """

        :param LLMclient:
        :param ctxManager:
        :param useGenPrompt:
        :return:
        """
        # Use the LLM to exec based on the context
        # ctxManager.add_user_message(self.prompt)
        if useGenPrompt:
            use_prompt = genPromptOP(self.prompt).execute(LLMclient, ctxManager)
        else:
            use_prompt = self.prompt
        ctxManager.add_user_message(use_prompt)


        res = chatModel.create_completion(
            LLMclient,
            temperature=0.1,
            top_p=0.9,
            max_tokens=100,
            messages=ctxManager.get_messages()
        )
        print("Executed results: ")
        print(res.choices[0].message.content)

        ctxManager.add_assistant_message(res.choices[0].message.content)
        return ctxManager



