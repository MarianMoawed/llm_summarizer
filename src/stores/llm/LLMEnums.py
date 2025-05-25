from enum import Enum

class LLMEnums(Enum):
   
    
    MODEL_PROVIDER_GROQ = "groq"
    MODEL_PROVIDER_HUGGINGFACE = "huggingface"
    MODEL_PROVIDER_LOCAL = "local"

class GroqEnums(Enum):
    
    USER= "user"
    SYSTEM= "system"
   