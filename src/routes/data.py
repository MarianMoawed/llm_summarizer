from fastapi import APIRouter, Request, UploadFile, File, Form
from fastapi.exceptions import HTTPException
from typing import Optional


data_router = APIRouter(prefix="/api/v1",tags=["data"])


@data_router.post("/upload/text")
def upload_text(file: Optional[UploadFile]=File(None),text: Optional[str] =None):
    if not text and not file:
        raise HTTPException(status_code=400, detail="Either text or file must be provided")
    if text:
        return {"text": text}