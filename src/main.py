from fastapi import FastAPI
from routes.base import base_router
from routes.data import data_router
from routes.nlp import nlp_router
from stores.llm.LLMFactory import LLMFactory
from helpers.config import get_settings
app = FastAPI()

settings = get_settings()
llm_factory=LLMFactory(settings,settings.GENERATION_BACKEND)

app.generation_client=llm_factory.create()
app.generation_client.set_generation_model(model_name=settings.LLM_GENERATION_MODEL)
app.include_router(base_router)
app.include_router(data_router)
app.include_router(nlp_router)