import os
import sys
from pathlib import Path
from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    # 环境相关
    project_env: str = os.getenv("PROJECT_ENV", "dev")
    is_dev: bool = project_env == "dev"

    # 目录配置
    base_dir = Path(__file__).absolute().parent
    log_dir = base_dir / 'logs'

    # url 的前缀
    url_prefix: str = "/api/v1"
    admin_url_prefix: str = f"{url_prefix}/admin"
    client_url_prefix: str = f"{url_prefix}/client"
    # host 配置
    server_host: str = '0.0.0.0'
    server_port: int = 8000
    # /docs 获取 token 的 url
    oauth2_token_url: str = "/test/auth/token"

    # 中间件配置
    # 跨域请求
    cors_origins: list[str] = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["PUT", 'POST', 'GET', 'DELETE', 'OPTIONS']
    cors_allow_headers: list[str] = ["*"]
    # 日志中间件的白名单，只填写去除 url_prefix 的部分
    logger_path_white_list: list[str] = [
        '/user/captcha', '/test/files', '/test/uploadfile']
    # TrustedHostMiddleware
    allowed_hosts = ["*"]

    # Mysql 配置
    mysql_db: str = os.getenv("MYSQL_DB")
    mysql_host: str = os.getenv("MYSQL_HOST")
    mysql_port: int = os.getenv("MYSQL_PORT")
    mysql_user: str = os.getenv("MYSQL_USER")
    mysql_pwd: str = os.getenv("MYSQL_PWD")

    # Redis 配置
    cache_redis_url: str = "redis://localhost:26379/0"
    # Session
    session_secret_key = "sadehewagbwft34ba"
    session_cookie = "session_id"
    session_max_age = 14 * 24 * 60 * 60
    # SetSessionMiddleware
    session_cookie_name = 'session'
    # 图片验证码有效时间
    captcha_seconds: int = 5 * 60
    # 图片验证码key
    captcha_key: str = 'captcha:{}'

    # jwt加密的盐   openssl rand -hex 32
    jwt_secret_key: str = "a489b1d15b4902c5e82086791c6a5820035c6b3eee5ee2759fd66931e486b5a9"
    # jwt加密算法
    jwt_algorithm: str = 'HS256'
    # token过期时间，单位：秒
    jwt_exp_seconds: int = 7 * 24 * 60 * 60

    @property
    def tortoise_orm_model_modules(self) -> List[str]:
        return ['aerich.models', 'service.models']

    @property
    def tortoise_orm_config(self) -> dict:
        return {
            "connections": {
                "default": {
                    'engine': 'tortoise.backends.mysql',
                    "credentials": {
                        'host': self.mysql_host,
                        'user': self.mysql_user,
                        'password': self.mysql_pwd,
                        'port': self.mysql_port,
                        'database': 'mall',
                    }
                }
            },
            "apps": {
                "base": {
                    "models": self.tortoise_orm_model_modules,
                    "default_connection": "default"
                },
            },
            'use_tz': False,
            'timezone': 'Asia/Shanghai'
        }

    @property
    def loguru_config(self):
        return {
            "handlers": [
                {
                    "sink": sys.stdout,
                    "level": "DEBUG",
                    "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | {thread.name} | "
                              "<level>{level}</level> | "
                              "<cyan>{module}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
                              "<level>{message}</level>"
                },
                {
                    "sink": self.log_dir / 'fastapi.log',
                    "level": "INFO",
                    "rotation": "10 MB",
                    "retention": "1 week",
                    "encoding": 'utf-8',
                    "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {thread.name} | {level} | "
                              "{module} : {function}:{line} -  {message}"
                },
                {
                    "sink": self.log_dir / 'fastapi-error.log',
                    "serialize": True,
                    "level": 'ERROR',
                    "retention": "1 week",
                    "rotation": "10 MB",
                    "encoding": 'utf-8',
                    "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {thread.name} | {level} | "
                              "{module} : {function}:{line} -  {message}"
                },
            ],
        }

    @property
    def log_config(self):
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": "%(asctime)s | %(levelname)7s | %(name)s | "
                              "%(module)s.%(funcName)s:%(lineno)d - %(message)s",
                    "use_colors": None
                },
                "simple": {
                    "format": "%(levelname)s %(message)s"
                }
            },
            "handlers": {
                "stderr": {
                    "level": "DEBUG",
                    "class": "logging.StreamHandler",
                    "formatter": "standard",
                    "stream": "ext://sys.stderr"
                },
                "stdout": {
                    "level": "DEBUG",
                    "class": "logging.StreamHandler",
                    "formatter": "standard",
                    "stream": "ext://sys.stdout"
                },
                "loguru": {
                    "class": "service.common.log.InterceptHandler"
                }
            },
            "loggers": {
                "fastapi": {
                    "handlers": [
                        "loguru"
                    ],
                    "level": "DEBUG"
                },
                "tortoise": {
                    "handlers": [
                        "loguru"
                    ],
                    "level": "DEBUG"
                },
                "apscheduler": {
                    "handlers": [
                        "loguru"
                    ],
                    "level": "INFO"
                },
                "uvicorn": {
                    "handlers": [
                        "loguru"
                    ],
                    "level": "INFO"
                },
                "uvicorn.error": {
                    "handlers": [
                        "loguru"
                    ],
                    "level": "INFO",
                    "propagate": False
                },
                "uvicorn.access": {
                    "handlers": [
                        "loguru"
                    ],
                    "level": "INFO",
                    "propagate": False
                }
            }
        }


settings = Settings()


if __name__ == '__main__':
    print(settings)
