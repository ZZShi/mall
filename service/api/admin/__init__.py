from fastapi import APIRouter

from service.config import settings
from service.api.admin.user import app as user

app = APIRouter(prefix=settings.admin_url_prefix, tags=["商城后台"])

app.include_router(user, tags=["用户管理"])
