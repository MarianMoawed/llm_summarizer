from enum import Enum

class LLMEnums(Enum):
   
    
    MODEL_PROVIDER_GROQ = "groq"
    MODEL_PROVIDER_HUGGINGFACE = "huggingface"
    MODEL_PROVIDER_LOCAL = "local"
    CHAT_HISTORY="summarize this text to 4 or 5 bullet points"


class GroqEnums(Enum):
    
    USER= "user"
    SYSTEM= "system"
   