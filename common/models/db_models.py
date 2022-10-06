from peewee import CharField, CompositeKey, DateTimeField, ForeignKeyField, IntegerField

from common.db.basic import BaseModel, EnumField
from common.enums import UserRole


class Project(BaseModel):
    project_id = CharField(primary_key=True, help_text='ID из гугл таблицы')
    project_name = CharField(unique=True)


class User(BaseModel):
    telegram_id = IntegerField(primary_key=True)


class ProjectToUser(BaseModel):
    project = ForeignKeyField(Project)
    user = ForeignKeyField(User)

    username = CharField()
    role = EnumField(enum=UserRole)

    class Meta:
        primary_key = CompositeKey('project', 'user')


class LastKnownState(BaseModel):
    project = ForeignKeyField(Project)
    sheet = CharField()

    street_name = CharField()
    last_known_status = CharField()

    error_description = CharField()

    last_seen_at = DateTimeField()
