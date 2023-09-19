import logging.config

import uvicorn
from loguru import logger
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from tortoise.contrib.fastapi import register_tortoise

from config import settings
from api import admin, client
from common.events import register_events
from common.exceptions import register_exceptions
from common.middlewares import register_middlewares

# 配置日志器
logger.configure(**settings.loguru_config)
logging.config.dictConfig(settings.log_config)


app = FastAPI(
    debug=settings.is_dev,
    default_response_class=ORJSONResponse
)

# 注册异常处理
register_exceptions(app)

# 注册中间件
register_middlewares(app)

# 注册数据库
register_tortoise(app, config=settings.tortoise_orm_config, generate_schemas=False)

# 注册事件
register_events(app)

# 注册路由
app.include_router(admin)
app.include_router(client)


@app.get("/", summary="首页")
async def root():
    return {"message": "Hello World"}


@app.get("/health_check", summary="健康检查")
async def say_hello():
    return {"message": f"I'm Healthy"}


if __name__ == '__main__':
    uvicorn.run(app="start:app", host=settings.server_host, port=settings.server_port, reload=settings.is_dev)
