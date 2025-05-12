DEFAULT_SYSTEM_PROMPT = """
You are a helpful assistant. You are provided with a question. Your task is to answer the question succinctly.
"""

class LLMContextManager:
    def __init__(self, initial_system_prompt=DEFAULT_SYSTEM_PROMPT):
        self.messages = [{"role": "system", "content": initial_system_prompt}]
        self.results = {}  # Store intermediate results
        
    def add_user_message(self, content):
        self.messages.append({"role": "user", "content": content})

    def add_assistant_message(self, content):
        self.messages.append({"role": "assistant", "content": content})

    def pop_latest_message(self):
        self.messages.pop()

    def get_messages(self):
        return self.messages
    
    def store_result(self, value, key):
        
        if not key:
            raise ValueError("Key cannot be None or empty.")
        if key in self.results:
            # Append the new value to the existing list
            self.results[key].append(value)
        else:
            # Initialize a new list with the value
            self.results[key] = [value]

    def retrieve_result(self, key):
        
        return self.results.get(key)

    def clear_results(self):
        
        self.results = {}
        if hasattr(self, 'named_results'):
            self.named_results.clear()