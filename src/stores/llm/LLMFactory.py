from stores.llm.providers.GroqProvider import GroqProvider
import logging
from .LLMEnums import LLMEnums




class LLMFactory:

    def __init__(self, config, provider_name: str):
        self.config = config
        self.provider_name = provider_name
        self.provider=None

    def create(self):
        if self.provider_name == LLMEnums.MODEL_PROVIDER_GROQ.value:
            self.provider= GroqProvider(api_key=self.config.GROQ_API_KEY,
                                default_max_tokens=self.config.LLM_DEFAULT_MAX_TOKENS,
                                default_temperature=self.config.LLM_DEFAULT_TEMPERATURE,
                                default_input_max_characters=self.config.DEFAULT_INPUT_MAX_CHARACTERS
                                ) 
            if self.provider==None:
                return  logging.ERROR("provider not supported {provider_name}")
            
        return self.provider

    