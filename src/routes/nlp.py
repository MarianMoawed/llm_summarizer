from fastapi import APIRouter,Request
from fastapi.responses import JSONResponse
from helpers.config import get_settings
from stores.llm.LLMEnums import LLMEnums
from model.enums.signalResponse import SignalResponse

settings=get_settings()

nlp_router=APIRouter(prefix="/api/v1/nlp",tags=['NLP'])
@nlp_router.post("/summarize/text")
def summarize_text(text,request:Request):

    if request.app.generation_client is None:
        return JSONResponse(
            status_code=400,
            content={SignalResponse.NONE_GENERATION_CLIENT.value}
        )
    
    response=request.app.generation_client.generate_text(
        prompt=text,
        max_tokens=settings.LLM_DEFAULT_MAX_TOKENS,
        temperature= settings.LLM_DEFAULT_TEMPERATURE,
        chat_history=LLMEnums.CHAT_HISTORY.value
        )
    return response