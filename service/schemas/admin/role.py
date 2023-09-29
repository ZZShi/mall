from typing import List, Optional

from fastapi import Query
from pydantic import BaseModel, Field

from service.common.resp import ORMModel


# -------------------------------  请求部分  ---------------------------------------------


class RoleCreate(BaseModel):
    """ 创建角色 """
    role_name: str = Field(..., alias='roleName')
    status: Optional[bool]
    order_no: Optional[int] = Field(None, alias='orderNo')
    remark: Optional[str]
    menu_values: Optional[List[int]] = Field([], alias='menu')


class RoleUpdate(RoleCreate):
    """ 更新角色 """


class RoleStatus(BaseModel):
    id: int = Field(..., gt=0)
    status: bool


class RoleFilter(BaseModel):
    """ 过滤角色 """
    role_name__icontains: str = Query(None, alias='roleName')
    remark__icontains: str = Query(None, alias='remark')


# -------------------------------  响应部分  ---------------------------------------------
class RoleInfoForLoginResp(ORMModel):
    """ 角色信息 用于响应登陆接口 实际返回的是不是超管，只是不想改前端代码而已，实际没什么用 """
    role_name: str = Field(..., alias='roleName', description="用户组")
    value: str = Field(..., description='用户组值')


class RoleInfoOptionItem(ORMModel):
    role_value: int = Field(..., alias='roleValue')
    role_name: str = Field(..., alias='roleName')


class RoleInfo(ORMModel):
    """ 角色信息 """
    role_value: int = Field(..., alias='roleValue')
    role_name: str = Field(..., alias='roleName')
    status: bool
    order_no: Optional[int] = Field(..., alias='orderNo')
    menu_values: Optional[List[int]] = Field([], alias='menu')
    remark: Optional[str]
