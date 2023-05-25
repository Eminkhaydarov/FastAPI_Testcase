import uuid

from pydantic import BaseModel


class CreateUserSchema(BaseModel):
    token: uuid.UUID