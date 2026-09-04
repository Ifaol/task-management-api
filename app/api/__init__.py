from fastapi import APIRouter

from app.api.tasks import router as tasks_router
from app.api.users import router as users_router


router = APIRouter()

router.include_router(tasks_router)
router.include_router(users_router)