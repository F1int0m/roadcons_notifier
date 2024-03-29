from peewee import CharField, Model
from peewee_async import Manager, PooledPostgresqlDatabase

pg_db = PooledPostgresqlDatabase(None)
manager = Manager(pg_db)


class BaseModel(Model):
    class Meta:
        database = pg_db

    @classmethod
    async def create(cls, **params) -> 'BaseModel':
        async with manager.atomic():
            return await manager.create(cls, **params)

    def is_changed(self, **kwargs):
        for name, value in kwargs.items():
            current_value = getattr(self, name)
            if current_value != value:
                return True
        return False

    async def update_instance(self, **params):
        new_params = {fld: val for fld, val in params.items() if fld in self._meta.fields}
        changed = self.is_changed(**new_params)
        if changed:
            for fld, value in new_params.items():
                setattr(self, fld, value)
            await manager.update(self)
        return changed


class EnumField(CharField):

    def __init__(self, enum, **kwargs):
        self._enum = enum
        self.value = None
        super().__init__(**kwargs)

    def db_value(self, value):
        assert type(value) == self._enum, f'Enum object {self._enum} expected, {type(value)} given'
        value = self._enum(value)
        return str(value.value)

    def python_value(self, value):
        return self._enum(value)
