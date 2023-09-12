import logging

import loguru
from fastapi import FastAPI


class LoguruHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        loguru.logger.opt(depth=6).log(record.levelno, log_entry)


app = FastAPI()

loguru_handler = LoguruHandler()
loguru_handler.setLevel(logging.DEBUG)

app.logger.handlers = [loguru_handler]


@app.get("/")
async def root():
    app.logger.debug("这是一个调试日志")
    app.logger.info("这是一个信息日志")
    app.logger.warning("这是一个警告日志")
    return {"message": "Hello, World!"}