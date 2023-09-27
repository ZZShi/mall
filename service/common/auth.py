import time
from datetime import datetime, timedelta

from starlette import status
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, Request, HTTPException

from service.models import User
from service.config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.admin_url_prefix}/user{settings.oauth2_token_url}")


def create_token(username: str) -> str:
    """通过加密算法获取到 token"""
    data = {
        "username": username,
        "exp": datetime.utcnow() + timedelta(seconds=settings.jwt_exp_seconds),
    }
    return jwt.encode(data, key=settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


async def get_user_by_token(token: str) -> User | None:
    """通过 token 获取 User 对象"""
    try:
        payload = jwt.decode(token, key=settings.jwt_secret_key, algorithms=settings.jwt_algorithm)
    except JWTError:
        return None
    exp = payload.get("exp")
    if exp and time.time() - exp > 0:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token 已过期，请重新登录",
            headers={"WWW-Authenticate": "Bearer"}
        )
    username = payload.get("username")
    if not username:
        return None
    else:
        return await User.get_or_none(username=username)


async def get_current_user(req: Request, token: str = Depends(oauth2_scheme)) -> User:
    """获取当前登录的用户信息"""
    user = await get_user_by_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token 已失效，请重新登陆！",
            headers={"WWW-Authenticate": "Bearer"}
        )
    if not user.status:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="账号已被禁用")
    req.state.user = user
    return user
