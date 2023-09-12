from datetime import datetime
from typing import TypeVar, Optional, Generic, List, Type

from pydantic import Field, BaseModel
from pydantic.generics import GenericModel
from tortoise.queryset import QuerySet


_T = TypeVar("_T")  # 响应的数据
_Model = TypeVar('_Model', bound='BaseModel')


class ORMModel(BaseModel):
    """ 带orm的pydantic模型 """
    id: int = Field(..., alias='id', description='自增 ID')

    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

    @classmethod
    async def from_queryset(cls: Type['_Model'], qs: QuerySet) -> List["_Model"]:
        return [cls.from_orm(x) for x in await qs]


class ResponseModel(GenericModel):
    """ 可以使用别名的响应模型 """

    class Config:
        allow_population_by_field_name = True


class RespFail(ResponseModel, Generic[_T]):
    """ 失败的响应 """
    code: int = Field(401, gt=0, description='状态码')
    msg: str = Field(..., description='信息摘要', alias='msg')
    data: Optional[_T] = Field(None, description='响应的数据', alias='data')


class RespSucc(ResponseModel, Generic[_T]):
    """ 成功的响应 """
    code: int = Field(200, description='状态码')
    msg: str = Field('success', description='信息摘要', alias='msg')
    data: Optional[_T] = Field(None, description='响应的数据', alias='data')


class RespSingle(RespSucc, Generic[_T]):
    """ 响应单个对象 """
    data: _T = Field(..., description='响应的数据', alias='data')


class RespMulti(RespSucc, Generic[_T]):
    """ 响应多个对象 """
    data: List[_T] = Field(..., description='响应的数据', alias='data')


class PageData(GenericModel, Generic[_T]):
    """ 分页响应的数据部分 """
    total: int = Field(..., description='总数量')
    items: List[_T] = Field(..., description='数据列表')


class RespPage(RespSucc, Generic[_T]):
    """ 分页响应 vben """
    data: PageData[_T] = Field(..., description='响应的数据', alias='data')
