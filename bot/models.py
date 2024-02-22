import re

from tortoise.models import Model
from tortoise import fields


class User(Model):
    user_id = fields.IntField(unique=True, pk=True)
    username = fields.CharField(max_length=255, null=True)
    full_name = fields.CharField(max_length=255)
    join_date = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "users"

    def __str__(self):
        return f"[{self.user_id}] {self.full_name}"


class Field(Model):
    field_id = fields.IntField(unique=True, pk=True)
    field_name = fields.CharField(max_length=255)
    field_re = fields.CharField(max_length=4095, null=True)

    class Meta:
        table = "fields"

    def __str__(self):
        return f"[{self.field_id}] {self.field_name}"

    def check_string(self, input_string: str) -> bool:
        if not self.field_re:
            return True

        regex = re.compile(str(self.field_re), re.I)
        match = regex.fullmatch(input_string)
        return bool(match)


class Template(Model):
    template_id = fields.IntField(unique=True, pk=True)
    template_name = fields.CharField(max_length=255)
    template_fields = fields.CharField(max_length=511)

    class Meta:
        table = "templates"

    def __str__(self):
        return f"[{self.template_id}] {self.template_name}"

    def get_fields_ids(self):
        return list(map(int, str(self.template_fields).split()))
