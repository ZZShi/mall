from typing import Union

from tortoise.queryset import F
from tortoise.exceptions import OperationalError
from tortoise.transactions import in_transaction
from fastapi import APIRouter, Depends, Request, Security

from service.common.deps import Paginator
from service.common.auth import check_permission
from service.models.user import OpLog, Role, Access
from service.common.resp import RespSucc, RespSingle, RespPage, RespFail
from service.schemas.admin.role import RoleCreate, RoleUpdate, RoleInfo, RoleFilter


app = APIRouter(prefix="/role", tags=["角色管理"])


@app.get('', summary='角色列表', response_model=RespPage[RoleInfo],
         dependencies=[Security(check_permission, scopes=["role_list"])])
async def lst(pg: Paginator() = Depends(), ft: RoleFilter = Depends(RoleFilter)):
    qs = Role.all().annotate(role_value=F('id')).prefetch_related('access').order_by('order_no')
    data = await pg.output(qs, ft.dict(exclude_defaults=True))
    return RespPage[RoleInfo](data=data)


@app.post('', summary='角色创建', dependencies=[Security(check_permission, scopes=["role_create"])])
async def create(p: RoleCreate, req: Request):
    await Role.create(**p.dict())
    await OpLog.add_log(req=req, user_id=req.state.user.id, remark=f"创建角色({p.role_name})")
    if p.menu_values:
        await Access.filter(status=True, id__in=p.menu_values).all()
        await OpLog.add_log(req=req, user_id=req.state.user.id, remark=f"分配权限({p.menu_values})")
    return RespSucc()


@app.get('/{pk}', summary='角色查询', response_model=Union[RespSingle[RoleInfo], RespFail],
         dependencies=[Security(check_permission, scopes=["role_search"])])
async def update(pk: int):
    item = await Role.annotate(role_value=F('id')).get_or_none(pk=pk)
    if not item:
        return RespFail(msg=f"查询的对象不存在 {pk=}")
    await item.fetch_related('access')
    data = RoleInfo.from_orm(item)
    return RespSingle[RoleInfo](data=data)


@app.put('/{pk}', summary='角色更新', response_model=Union[RespSucc, RespFail],
         dependencies=[Security(check_permission, scopes=["role_update"])])
async def update(pk: int, p: RoleUpdate, req: Request):
    item = await Role.get_or_none(pk=pk)
    if not item:
        return RespFail(msg=f"更新的对象不存在 {pk=}")
    try:
        async with in_transaction():
            await item.update_from_dict(p.dict(exclude_unset=True, exclude_none=True))
            await item.save()
            await OpLog.add_log(req=req, user_id=req.state.user.id, remark=f"角色更新")
            await item.access.clear()
            if p.menu_values:
                # todo
                ...
    except OperationalError:
        return RespFail(msg="更新失败")
    return RespSucc(msg="更新成功")


@app.delete('/{pk}', summary='角色删除', response_model=Union[RespSucc, RespFail],
            dependencies=[Security(check_permission, scopes=["role_delete"])])
async def delete(pk: int, req: Request):
    item = await Role.get_or_none(pk=pk)
    if not item:
        return RespFail(msg=f"删除的对象不存在 {pk=}")
    await item.delete()
    await OpLog.add_log(req=req, user_id=req.state.user.id, remark=f"角色删除")
    return RespSucc(msg="删除成功")
