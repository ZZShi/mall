import random
from typing import Union

import requests as requests
from redis import Redis
from simpel_captcha import img_captcha
# from starlette.responses import StreamingResponse
from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm

from service.common.auth import create_token, get_current_user
from service.common.deps import get_captcha_code, get_redis
from service.config import settings
from service.models.user import User
from service.common.resp import RespSucc, RespFail, RespSingle
from service.schemas.admin.user import UserLogin, UserInfo, UserRegister, ModifyPassword, ModifyInfo

app = APIRouter(prefix="/user", tags=["用户中心"])


@app.post(f"{settings.oauth2_token_url}", summary="文档登录,调试使用")
async def get_items(p: OAuth2PasswordRequestForm = Depends()):
    user = await User.get_or_none(username=p.username)
    if not user:
        return RespFail(msg="用户名不存在")
    if not user.check_password(p.password):
        return RespFail(msg="密码错误")
    token = create_token(username=p.username)
    return {"access_token": token, "token_type": "bearer"}


# @app.post('/register', response_model=Union[RespSingle[UserInfo], RespFail], summary='用户注册')
# async def register(post: UserRegister, code_in_redis: str = Depends(get_captcha_code)):
#     """用户注册不适用于后台系统，在前台系统中使用"""
#     if code_in_redis is None:
#         return RespFail(code=10302, msg='验证码已过期')
#     if post.code.lower() != code_in_redis:
#         return RespFail(code=10303, msg='验证码错误')
#     if await User.filter(username=post.username).exists():
#         return RespFail(code=10101, msg='当前用户名已被占用')
#     user = await User.create(**post.dict())
#     await user.set_password(post.password)
#     user_info = UserInfo.from_orm(user)
#     return RespSingle[UserInfo](data=user_info)


@app.get("/captcha", summary='图片验证码')
def image_captcha(req: Request, redis: Redis = Depends(get_redis)):
    image, text = img_captcha(byte_stream=True)
    session_value = req.session.get(settings.session_cookie_name)
    key = settings.captcha_key.format(session_value)
    redis.setex(name=key, time=settings.captcha_seconds, value=text.lower())    # 异步会报错，所以此处改为同步
    # return StreamingResponse(content=image, media_type='image/jpeg')
    return RespSucc(data={"code": text, "session": key})


@app.post('', response_model=Union[RespSingle[UserInfo], RespFail], summary='创建用户')
async def create(post: UserRegister):
    if await User.filter(username=post.username).exists():
        return RespFail(code=10101, msg='当前用户名已被占用')
    hero_list = requests.get("https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js").json()["hero"]
    hero = random.choice(hero_list)
    info = {
        "nickname": hero["name"],
        "full_name": hero["title"],
        "head_img": f"https://game.gtimg.cn/images/lol/act/img/champion/{hero['alias']}.png",
    }
    user = await User.create(**post.dict(), **info)
    await user.set_password(post.password)
    user_info = UserInfo.from_orm(user)
    return RespSingle[UserInfo](data=user_info)


@app.post("/login", response_model=RespSucc, summary="用户登录")
async def get_items(p: UserLogin, code: str = Depends(get_captcha_code)):
    # 跳过验证吗验证
    # if not code:
    #     return RespFail(msg="验证码已过期")
    # if p.code.lower() != code.lower():
    #     return RespFail(msg="验证码输入错误")
    user = await User.get_or_none(username=p.username)
    if not user:
        return RespFail(msg="用户名不存在")
    if not user.check_password(p.password):
        return RespFail(msg="密码错误")
    token = create_token(username=p.username)
    return RespSucc(data={"token": token, "code": code})


@app.get('', response_model=Union[RespSingle[UserInfo], RespFail], summary='查看个人信息')
async def get_my_info(me: User = Depends(get_current_user)):
    return RespSingle[UserInfo](data=me)


@app.put('', response_model=Union[RespSingle[UserInfo], RespFail], summary='修改个人信息')
async def foo(p: ModifyInfo, me: User = Depends(get_current_user)):
    await me.update_from_dict(p.dict(exclude_unset=True, exclude_none=True))
    await me.save()
    return RespSucc[UserInfo](data=me)


@app.put('/password', response_model=Union[RespSucc, RespFail], summary='修改个人密码')
async def foo(p: ModifyPassword, me: User = Depends(get_current_user)):
    if not me.check_password(p.old_password):
        return RespFail(msg="密码错误")
    await me.set_password(p.new_password)
    return RespSucc(msg="密码修改成功")
