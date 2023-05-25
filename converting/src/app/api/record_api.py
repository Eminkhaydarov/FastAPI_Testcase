import uuid

from fastapi import APIRouter, Depends, UploadFile, File, Request, Query

from src.app.schemas.record_schema import UploadSchema
from src.app.service.record_service import RecordService

router = APIRouter(prefix='/record')


@router.get('/')
async def get_mp3(audio_id: uuid.UUID = Query(...), user_id: int = Query(...), service: RecordService = Depends()):
    return await service.get_record(audio_id=audio_id, user_id=user_id)


@router.post('/', response_model=UploadSchema)
async def convert_record(request: Request, user_id: int, token: uuid.UUID, file: UploadFile = File(...),
                         service: RecordService = Depends()):
    audio_id, user_id = await service.convert_record(user_id, token, file)
    base_url = str(request.base_url)
    full_url = f"{base_url}api/record/?audio_id={audio_id}&user_id={user_id}"
    return {'download_link': full_url}
