import asyncio
from functools import lru_cache
from typing import List, Optional, Dict

import redis
from redis import Redis
from tortoise.queryset import QuerySet
from fastapi import Query, Depends, Request

from service.config import settings
from service.common.resp import PageData


class Paginator:
    """分页器"""
    def __init__(self, max_size: int = 100):
        self.max_size = max_size
        self.page_num: int = 1
        self.page_size: int = 10
        self.order: List[str] = ['id']

    def __call__(self, page_num: int = Query(1, description='当前页码', alias='page'),
                 page_size: int = Query(10, description='每页数量', alias='size'),
                 order: List[str] = Query(['id'], description='按指定字段排序，格式：id 或 -create_time')):
        self.order = order
        self.page_num = max(page_num, 1)  # 如果传入的值小于1，按 1 算
        self.page_size = min(page_size, self.max_size)  # 如果超过 max_size ， 就算做是 maxsize
        return self

    async def output(self, queryset: QuerySet, filters: Optional[Dict] = None):
        if filters is None:
            filters = {}
        total, items = await asyncio.gather(
                queryset.filter(**filters).count(),
                queryset.limit(self.limit).offset(self.offset).order_by(*self.order).filter(**filters),
                )
        return PageData(items=items, total=total)

    @property
    def limit(self):
        return self.page_size

    @property
    def offset(self):
        return self.page_size * (self.page_num - 1)


@lru_cache()
def get_redis() -> Redis:
    return redis.from_url(settings.cache_redis_url, encoding='utf-8', decode_responses=True)


def get_session_value(req: Request):
    return req.session.get(settings.session_cookie_name)


def get_captcha_code(session_value: str = Depends(get_session_value),
                     r: Redis = Depends(get_redis)) -> str | None:
    if not session_value:
        return
    key = settings.captcha_key.format(session_value)
    code_in_redis = r.get(key)
    return code_in_redis
