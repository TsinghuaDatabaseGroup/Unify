"""
    Input the description of the task and the current ctx, and let the LLM generate a prompt to solve this task
"""

GEN_PROMPT_PROMPT = """
    In order to let LLM finish the following task "{}".
    Please write the corresponding prompt. 
    Please do not output any explanation or reasoning, just write the prompt. 
    Your output will directly be used as the prompt for the next step. 
"""

class genPromptOP:
    def __init__(self, taskDescription):
        self.taskDescription = taskDescription
        self.opName = "GenPrompt"

    def execute(self, LLMclient, chatModel, ctxManager):
        """ctxManager should not be modified after execution here!"""

        input_prompt = GEN_PROMPT_PROMPT.format(self.taskDescription)
        ctxManager.add_user_message(input_prompt)

        res = chatModel.create_completion(
            LLMclient,
            temperature=0.1,
            top_p=0.9,
            max_tokens=100,
            messages=ctxManager.get_messages()
        )
        generatedPrompt = res.choices[0].message.content

        print("## Current OP: ", self.opName)
        print("### Generated Prompt: ")
        print(generatedPrompt)

        ctxManager.pop_latest_message()
        return generatedPrompt



