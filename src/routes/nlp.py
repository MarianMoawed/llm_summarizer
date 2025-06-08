from fastapi import APIRouter,Request
from fastapi.responses import JSONResponse
from helpers.config import get_settings
from stores.llm.LLMEnums import LLMEnums
from model.enums.signalResponse import SignalResponse
from model.AssetModel import AssetModel
from model.ChunkModel import ChunkModel

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


@nlp_router.post("/summarize/{project_id}")
async def summarize_file(request: Request,project_id:str, file_id: str):

    asset_model = await AssetModel.create_instance(db_client=request.app.db_client)
    asset = await asset_model.get_asset_record(asset_project_id=project_id, asset_name=file_id)

    chunk_model = await ChunkModel.create_instance(db_client=request.app.db_client)
    asset_chunks = await chunk_model.get_asset_chunks(project_id=project_id, asset_id=asset.id)

    full_text = " ".join(chunk.chunk_content for chunk in asset_chunks)
    summary =  request.app.generation_client.generate_text(
        prompt=full_text,
        max_tokens=settings.LLM_DEFAULT_MAX_TOKENS,
        temperature= settings.LLM_DEFAULT_TEMPERATURE,
        chat_history=LLMEnums.CHAT_HISTORY.value
    )
    return JSONResponse(content={"summary": summary})