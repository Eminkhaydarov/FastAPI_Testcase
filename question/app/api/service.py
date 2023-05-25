from datetime import datetime

from sqlalchemy.exc import ProgrammingError

import app.main as main
from typing import List, Dict, Union

from fastapi import Depends, HTTPException

from sqlalchemy import select, desc
from sqlalchemy.orm import Session
import aiohttp

from app.api.models import QuestionModel
from app.api.schema import QuestionSchema
from app.database import get_async_session


class QuestionService:

    def __init__(self, session: Session = Depends(get_async_session)):
        self.session = session

    @classmethod
    async def get_question(cls, url: str) -> List[Dict[str, Union[int, str]]]:
        async with main.aiohttp_session.get(url) as response:
            resp = await response.json()
            result = [{
                'id': i['id'],
                'question': i['question'],
                'answer': i['answer'],
                'created_at': i['created_at']}
                for i in resp
            ]
            return result

    async def post(self, question_num: int) -> Union[QuestionSchema, list]:
        async with self.session as session:
            try:
                stmt = select(QuestionModel).order_by(desc(QuestionModel.add_at)).limit(1)
                last_item = await session.execute(stmt)
            except ProgrammingError:
                last_item = None
            attempts = 0
            MAX_ATTEMPTS = 15
            questions = []
            while len(questions) < question_num and attempts < MAX_ATTEMPTS:
                attempts += 1
                question_count = question_num - len(questions)
                if question_count == 0:
                    break
                url_for_get = f'https://jservice.io/api/random?count={question_count}'
                try:
                    new_questions = await self.get_question(url_for_get)
                except aiohttp.ClientError as e:
                    raise HTTPException(status_code=503, detail="Service unavailable")
                for new_question in new_questions:
                    try:
                        query = select(QuestionModel).where(QuestionModel.id == new_question['id'])
                        result = await session.execute(query)
                        existing_question = result.scalar_one_or_none()
                    except ProgrammingError:
                        existing_question = None
                    if not existing_question:
                        questions.append(new_question)
        questions_for_add = [QuestionModel(id=question['id'],
                                           question=question['question'],
                                           answer=question['answer'],
                                           created_at=datetime.fromisoformat(question['created_at']),) for question in questions]
        session.add_all(questions_for_add)
        await session.commit()
        last_question = last_item.scalar_one_or_none()
        print(last_question)
        if last_question:
            return QuestionSchema(
                id=last_question.id,
                question=last_question.question,
                answer=last_question.answer,
                created_at=last_question.created_at
            )
        else:
            return {}
