from fastapi import APIRouter

from service.common.resp import RespSucc
from service.schemas.admin.user import UserLogin

app = APIRouter(prefix="/user")


# @app.get("/{pk}", response_model=RespSucc, summary="创建用户")
# async def get_items(pk: int):
#     ...


@app.post("/login", response_model=RespSucc, summary="用户登录")
async def get_items(p: UserLogin):
    data = p.dict()
    data.update(token="1234567")
    return RespSucc(data=data)
