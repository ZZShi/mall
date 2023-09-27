from fastapi import APIRouter

from service.config import settings
from service.api.admin.user import app as user

app = APIRouter(prefix=settings.admin_url_prefix)

app.include_router(user)
