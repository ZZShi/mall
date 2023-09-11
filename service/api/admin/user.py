from fastapi import APIRouter

from service.common import RespSucc
from service.schemas.admin.user import UserLogin

app = APIRouter(prefix="/user")


@app.get("/{pk}", response_model=RespSucc, summary="创建用户")
async def get_items(pk: int):
    ...


@app.get("/login", response_model=RespSucc, summary="用户登录")
async def get_items(p: UserLogin):
    data = p.dict()
    return RespSucc(data=data)
