from LLMInterface import LLMInterface
from groq import Groq
import logging
from LLMEnums import GroqEnums


class GroqProvider(LLMInterface):
    def __init__(self, api_key:str,default_input_max_characters:int=1000, default_max_tokens: int = 1000,default_temperature: float = 0.1):
       self.api_key = api_key
       self.generation_model_name = None
       self.default_max_tokens = default_max_tokens
       self.default_temperature = default_temperature
       self.default_input_max_characters = default_input_max_characters
       
       self.logger = logging.getLogger(__name__)

       self.client= Groq(api_key)

    def process_text(self, text: str) -> str:
        return text[:self.default_input_max_characters].strip()

    def set_generation_model(self, model_name: str):
        self.generation_model_name = model_name

    def generate_text(self, prompt:str,chat_history:list[str] , max_tokens:int=None, temperature:float=None  ) -> str:
        
        if self.client is None:

            self.logger.error("Groq client is not initialized.")
            return None
        
        if self.generation_model_name is None:

            self.logger.error("Model name is not set.")
            return None
        
        response = self.client.chat.completions.create(
            model= self.generation_model_name,
            messages =[
                        {"role":GroqEnums.SYSTEM,"content":chat_history},
                        {"role": GroqEnums.USER, "content": self.process_text(prompt)}
                      ] ,
            max_tokens= max_tokens if max_tokens is not None else self.max_tokens,
            temperature=temperature if temperature is not None else self.temperature
        )
        
        if response is None or response.choices is None or len(response.choices) == 0 or response.choices[0].message is None or response.choices[0].message.content is None:
            self.logger.error("Failed to get a response from Groq.")
            return None
        return response.choices[0].message.content.strip()
    
    def construct_prompt(self, prompt: str, role:str) -> str:
        return{
            "role": role,
            "content": prompt
        }
        