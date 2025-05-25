from providers import GroqProvider




class LLMFactory:
    def __init__(self,config, provider_name:str):
         
         self.config = config
         if provider_name == "groq":
            self.provider= GroqProvider(api_key=config.GROQ_API_KEY,
                                        default_max_tokens=config.LLM_DEFAULT_MAX_TOKENS,
                                        default_temperature=config.LLM_DEFAULT_TEMPERATURE,
                                        default_input_max_characters=config.DEFAULT_INPUT_MAX_CHARACTERS
                                        )
            
         return None

    