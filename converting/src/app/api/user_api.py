import uuid
from fastapi import APIRouter, Depends

from src.app.schemas.user_schema import CreateUserSchema
from src.app.service.user_service import UserService

router = APIRouter(prefix='/user')


@router.post('/', response_model=CreateUserSchema)
async def create_user(username: str, service: UserService = Depends()):
    return await service.create_user(username)
