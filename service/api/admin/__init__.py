from fastapi import APIRouter

from service.config import settings
from service.api.admin.user import app as user
from service.api.admin.role import app as role
from service.api.admin.access import app as access

app = APIRouter(prefix=settings.admin_url_prefix)

app.include_router(user)
app.include_router(role)
app.include_router(access)
