import os
import sys
from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    # 环境相关
    project_env: str = os.getenv("PROJECT_ENV", "dev")
    is_dev: bool = project_env == "dev"

    # 目录配置
    base_dir = Path(__file__).absolute().parent
    log_dir = base_dir / 'logs'

    # url的前缀
    url_prefix: str = "/api/v1"
    admin_url_prefix: str = f"{url_prefix}/admin"
    client_url_prefix: str = f"{url_prefix}/client"
    # host
    server_host: str = '0.0.0.0'
    server_port: int = 8000

    # 中间件配置
    # 跨域请求
    cors_origins: list[str] = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["PUT", 'POST', 'GET', 'DELETE', 'OPTIONS']
    cors_allow_headers: list[str] = ["*"]
    # Session
    session_secret_key = "sadehewagbwft34ba"
    session_cookie = "session_id"
    session_max_age = 14 * 24 * 60 * 60
    # SetSessionMiddleware
    session_cookie_name = 'session'
    # 日志中间件的白名单，只填写去除 url_prefix 的部分
    logger_path_white_list: list[str] = [
        '/user/captcha', '/test/files', '/test/uploadfile']
    # TrustedHostMiddleware
    allowed_hosts = ["*"]

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
                    "level": "WARNING"
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
