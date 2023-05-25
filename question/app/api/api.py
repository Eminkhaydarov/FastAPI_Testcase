from typing import Union

from fastapi import APIRouter, Depends

from app.api.schema import QuestionSchema
from app.api.service import QuestionService


from app.api.models import QuestionModel
from pydantic.types import conint

router = APIRouter(prefix='/question')


@router.post('/', response_model=Union[QuestionSchema, dict])
async def post(question_num: conint(ge=0, le=100), service: QuestionService = Depends())-> QuestionSchema:
    return await service.post(question_num)
