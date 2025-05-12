from utils.contextManager import LLMContextManager
import os


class ModelConfig:
    def __init__(self, model_path=None):
        # Default model path, can be adjusted according to the actual environment
        self.model_path = model_path or "/home/fit/liguol/Macly/Meta-Llama-3.1-70B-Instruct"
        self.validate_model_path()

    def validate_model_path(self):
        """Validate the model path"""
        if not self.model_path.startswith("http") and not os.path.exists(self.model_path):
            print(f"Warning: Model path {self.model_path} does not exist. Using default.")
            self.model_path = "/home/fit/liguol/Macly/Meta-Llama-3.1-70B-Instruct"

    def create_completion(self, client, temperature=0.1, top_p=0.9, max_tokens=1000, messages=None):
        """Unified LLM call method, using stored model configuration"""
        try:
            response = client.chat.completions.create(
                model=self.model_path,
                messages=messages,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens
            ).choices[0].message.content
            return response
        except Exception as e:
            print(f"LLM call failed: {e}. Using default model.")
            default_config = ModelConfig()
            return client.chat.completions.create(
                model=default_config.model_path,
                messages=messages,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens
            ).choices[0].message.content

# Default debug model configuration
DEBUG_MODEL_CONFIG = ModelConfig(
    model_path="/home/fit/liguol/Macly/Meta-Llama-3.1-70B-Instruct"
)
