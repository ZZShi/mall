from fastapi import APIRouter

from service.config import settings

app = APIRouter(prefix=settings.client_url_prefix, tags=["商城客户端"])
