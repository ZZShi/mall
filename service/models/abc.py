from tortoise import fields, Model


class TortoiseBaseModel(Model):
    created_time = fields.DatetimeField(auto_now_add=True, description='创建时间')
    updated_time = fields.DatetimeField(auto_now=True, description="更新时间")
    status = fields.BooleanField(default=True, description='True:启用 False:禁用')
    remark = fields.CharField(null=True, max_length=255, description="备注描述")

    class Meta:
        abstract = True
