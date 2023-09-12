import time

from loguru import logger
from fastapi import Request, FastAPI
from starlette.datastructures import MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from service.config import settings
from service.common.utils import random_str


class ProcessTime:
    """Middleware"""
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":  # 非http协议
            await self.app(scope, receive, send)
            return
        start_time = time.time()
        req = Request(scope, receive, send)
        if not req.session.get(settings.session_cookie_name):
            req.session.setdefault(settings.session_cookie_name, random_str())

        async def send_wrapper(message: Message) -> None:
            process_time = (time.time() - start_time) * 1000
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers.append("X-Process-Time", f"{process_time:.3f}ms")
            await send(message)

        await self.app(scope, receive, send_wrapper)


class ConsumeBodyMiddleware:
    """ 可以多次消费诗体 """
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":  # 非http协议
            await self.app(scope, receive, send)
            return
        # 放行白名单中的路径，流响应和请求，如果不放行，会阻塞
        scope_path = scope['path']
        api_path = scope['path'].replace(settings.url_prefix, '')
        if (not scope_path.startswith(settings.url_prefix)) or (api_path in settings.logger_path_white_list):
            await self.app(scope, receive, send)
            return

        # 以下三行保证请求体可以反复消费
        receive_ = await receive()

        async def receive():
            return receive_

        await self.app(scope, receive, send)


class LogReqResMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        """ 记录请求体和响应体 """
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ("http",):  # pragma: no cover
            await self.app(scope, receive, send)
            return

        scope_path = scope['path']
        api_path = scope['path'].replace(settings.url_prefix, '')
        if (not scope_path.startswith(settings.url_prefix)) or (api_path in settings.logger_path_white_list):
            await self.app(scope, receive, send)
            return

        if scope.get('server')[0] == 'test':
            await self.app(scope, receive, send)
            return

        receive_ = await receive()

        logger.debug(f"{self.__class__.__name__} request body: {receive_.get('body').decode()}")

        async def receive():
            return receive_

        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.body":
                logger.debug(f"{self.__class__.__name__} response body: {message.get('body').decode()}")
            await send(message)

        await self.app(scope, receive, send_wrapper)


class ProcessTimeMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        """ 在响应头中记录响应时间 """
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":  # 非http协议
            await self.app(scope, receive, send)
            return
        start_time = time.time()

        async def send_wrapper(message: Message) -> None:
            process_time = time.time() - start_time
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers.append("X-Process-Time", str(process_time))
            await send(message)

        await self.app(scope, receive, send_wrapper)


class SetSessionMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        """ 设置一个随机字符串的session """
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":  # 非http协议
            await self.app(scope, receive, send)
            return

        req = Request(scope, receive, send)
        if not req.session.get(settings.session_cookie_name):
            req.session.setdefault(settings.session_cookie_name, random_str())

        await self.app(scope, receive, send)


def register_middlewares(app: FastAPI):
    """注册中间件，先注册的在内层，洋葱模型"""
    app.add_middleware(ProcessTimeMiddleware)
    app.add_middleware(LogReqResMiddleware)
    app.add_middleware(SetSessionMiddleware)
    app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins,
                       allow_credentials=settings.cors_allow_credentials,
                       allow_methods=settings.cors_allow_methods,
                       allow_headers=settings.cors_allow_headers)
    app.add_middleware(SessionMiddleware, secret_key=settings.session_secret_key,
                       session_cookie=settings.session_cookie,
                       max_age=settings.session_max_age)
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.allowed_hosts)
