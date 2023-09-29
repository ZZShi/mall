from typing import Union

from tortoise.queryset import F
from tortoise.exceptions import OperationalError
from tortoise.transactions import in_transaction
from fastapi import APIRouter, Depends, Request, Security

from service.common.deps import Paginator
from service.common.auth import check_permission, get_current_user
from service.common.utils import make_tree
from service.models.user import OpLog, Role, Access, User
from service.common.resp import RespSucc, RespSingle, RespPage, RespFail
from service.schemas.admin.role import RoleCreate, RoleUpdate, RoleInfo, RoleFilter


app = APIRouter(prefix="/access", tags=["权限管理"])


@app.get('/router_tree', summary='获取前端路由')
async def tree(me: User = Depends(get_current_user)):
    if me.is_superuser:
        user_menu_ids = await Access.all().values_list('id', flat=True)
    else:
        user_menu_ids = await Access.filter(role__user__id=me.pk).values_list('id', flat=True)
    all_menu_list = [{
        "id": obj.pk,
        "path": obj.path,
        "name": obj.name,
        "component": obj.component,
        "redirect": obj.redirect,
        "order_no": obj.order_no,
        "parent_id": obj.parent_id,
        "meta": {
            "icon": obj.icon,
            "title": obj.title,
            "hideMenu": obj.hide_menu,
            "hideChildrenInMenu": obj.hide_children_in_menu,
        },
    } for obj in await Access.filter(is_router=True).all()]

    result_list = []

    def get_all_menu(menu_ids):
        if not menu_ids:
            return
        temp = []
        for menu_id in menu_ids:
            for menu_item in all_menu_list:
                if menu_id == menu_item['id']:
                    if menu_item not in result_list:
                        result_list.append(menu_item)
                    if menu_item['parent_id'] != 0:
                        temp.append(menu_item['parent_id'])
        get_all_menu(temp)

    get_all_menu(user_menu_ids)
    result_list.sort(key=lambda x: x['order_no'])
    result_list = make_tree(result_list, key_key='id')
    return RespSucc(data=result_list)
