import uuid
from starlette import status
from fastapi import Depends, HTTPException
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.app.models import User
from src.database import get_async_session


class UserService:

    def __init__(self, session: Session = Depends(get_async_session)):
        self.session = session

    async def create_user(self, username: str) -> uuid.UUID:

        user_uuid = uuid.uuid4()
        query = insert(User).values(username=username,
                                    uuid=user_uuid)

        async with self.session.begin():
            try:
                await self.session.execute(query)
                self.session.commit()
            except IntegrityError:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail="User with this username already exists")

        return {'token': user_uuid}
