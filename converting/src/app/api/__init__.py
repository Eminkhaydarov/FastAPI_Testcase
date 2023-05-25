from fastapi import APIRouter
from . import (record_api,
               user_api)

router = APIRouter(prefix='/api')
router.include_router(record_api.router)
router.include_router(user_api.router)