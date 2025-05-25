from abc import ABC, abstractmethod



class LLMInterface(ABC):

    @abstractmethod
    def set_generation_model(self, model_name: str):
        pass

    @abstractmethod
    def generate_text(self, prompt:str, max_tokens:int, temperature:float, chat_history:list[str]  ) -> str:
        pass

    @abstractmethod
    def construct_prompt(self, prompt: str, role:str) -> str:
        pass
    