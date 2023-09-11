import uvicorn
from fastapi import FastAPI

from service.config import settings
from service.api.admin import app as admin
from service.api.client import app as client


app = FastAPI()

# 注册路由
app.include_router(admin)
app.include_router(client)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health_check")
async def say_hello():
    return {"message": f"I'm Healthy"}


if __name__ == '__main__':
    uvicorn.run(app="start:app", host=settings.server_host, port=settings.server_port, reload=not settings.is_prod)
