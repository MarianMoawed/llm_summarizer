from pydantic_settings import BaseSettings

class Settings(BaseSettings):
   
   APP_NAME: str
   APP_VERSION: str

   FILE_TYPES:list

   GENERATION_BACKEND: str
   GROQ_API_KEY: str

   LLM_GENERATION_MODEL: str

   LLM_DEFAULT_TEMPERATURE: float 
   LLM_DEFAULT_MAX_TOKENS: int
   DEFAULT_INPUT_MAX_CHARACTERS: int

  

   DB_URL:str
   DB_NAME : str

   class Config:
        env_file = ".env"

def get_settings():
    return Settings()
        