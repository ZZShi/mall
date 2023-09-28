from enum import Enum, unique, IntEnum


@unique
class OpMethod(Enum):
    login_by_account = "账号登陆"
    change_password = "修改密码"

    read_object = "读取对象"
    list_objects = "对象列表"
    create_object = "创建对象"
    delete_object = "删除对象"
    update_object = "修改对象"
    change_status = "改变状态"
    allocate_resources = "分配资源"


@unique
class OpObject(Enum):
    user = "用户"
    account = "账号"
    role = "角色"
    menu = "菜单"
    profile = "用户资料"


class UserGender(IntEnum):
    unknown = 0     # 未知
    male = 1        # 男
    female = 2      # 女
