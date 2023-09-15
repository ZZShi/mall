from typing import Union

from fastapi import APIRouter, Depends

from service.common.deps import get_captcha_code
from service.models.user import User
from service.common.resp import RespSucc, RespFail, RespSingle
from service.schemas.admin.user import UserLogin, UserInfo, UserRegister

app = APIRouter(prefix="/user", tags=["用户中心"])


@app.post('', response_model=Union[RespSingle[UserInfo], RespFail], summary='用户注册')
async def register(post: UserRegister, code_in_redis: str = Depends(get_captcha_code)):
    if code_in_redis is None:
        return RespFail(code=10302, msg='验证码已过期')
    if post.code.lower() != code_in_redis:
        return RespFail(code=10303, msg='验证码错误')
    if await User.filter(username=post.username).exists():
        return RespFail(code=10101, msg='当前用户名已被占用')
    user = await User.create(**post.dict())
    await user.set_password(post.password)
    user_info = UserInfo.from_orm(user)
    return RespSingle[UserInfo](data=user_info)


@app.post("/login", response_model=RespSucc, summary="用户登录")
async def get_items(p: UserLogin):
    data = p.dict()
    data.update(token="1234567")
    return RespSucc(data=data)
