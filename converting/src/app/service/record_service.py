import asyncio
import concurrent
import os
import uuid
from typing import Tuple, Any
from uuid import UUID

from fastapi import Depends, HTTPException, UploadFile, File
from pydantic import AnyUrl
from sqlalchemy import select, insert
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from starlette import status
from src.app.models import Record, User
from src.app.utils import convert_to_mp3
from src.database import get_async_session
import src.main as main


class RecordService:

    def __init__(self, session: Session = Depends(get_async_session)):
        self.session = session

    async def get_record(self, audio_id: uuid.UUID, user_id: int) -> FileResponse:
        async with self.session.begin():
            query = select(Record).where(Record.uuid == audio_id, Record.user_id == user_id)
            result = await self.session.execute(query)
            result = result.scalar_one_or_none()
            if result is not None:
                return FileResponse(result.path, filename=f'{audio_id}.mp3')
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Record not found')

    async def convert_record(self, user_id: int, user_uuid: uuid.UUID, file: UploadFile) -> tuple[UUID, int]:
        async with self.session.begin():
            query = select(User).where(User.id == user_id)
            user = await self.session.execute(query)
            user = user.scalar_one_or_none()
            if not user:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect user id')
            if user.uuid != user_uuid:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid token')
            if not file.content_type in ('audio/wav', 'audio/x-wav'):
                raise HTTPException(status_code=400, detail="The file must be in WAV format.")
            record_uuid = uuid.uuid4()
            filepath = os.path.join('src', 'static', file.filename)
            with open(filepath, "wb") as buffer:
                buffer.write(await file.read())

            loop = asyncio.get_event_loop()
            with concurrent.futures.ProcessPoolExecutor() as pool:
                result = await loop.run_in_executor(pool, convert_to_mp3, filepath, record_uuid)
            path = result
            smtm = insert(Record).values(uuid=record_uuid, user_id=user.id, path=path)
            await self.session.execute(smtm)
            self.session.commit()
            return record_uuid, user.id
