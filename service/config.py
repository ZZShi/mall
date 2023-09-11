import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    project_env: str = os.getenv("PROJECT_ENV", "dev")
    is_prod: bool = project_env != "dev"

    # url的前缀
    admin_url_prefix: str = "/api/v1/admin"
    client_url_prefix: str = "/api/v1/client"
    # host
    server_host: str = '0.0.0.0'
    server_port: int = 8000


settings = Settings()


if __name__ == '__main__':
    print(settings)
