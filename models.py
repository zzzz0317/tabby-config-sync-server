import datetime
import json

import peewee

with open("config.json", "r", encoding="utf-8") as f_config_json:
    db_config_data = json.load(f_config_json).get("database", {})

db_type = db_config_data.get("db_type", "sqlite").lower()
db_name = db_config_data.get("db_name", "tabbyss.db")
db_host = db_config_data.get("db_host", "127.0.0.1")
db_port = int(db_config_data.get("db_port", "3306"))
db_user = db_config_data.get("db_user", "tabbyss")
db_pass = db_config_data.get("db_pass", "tabbyss")

if db_type == "sqlite":
    database = peewee.SqliteDatabase(db_name)
elif db_type == "mysql":
    database = peewee.MySQLDatabase(db_name, user=db_user, password=db_pass,
                                    host=db_host, port=db_port)
elif db_type == "postgresql":
    database = peewee.PostgresqlDatabase(db_name, user=db_user, password=db_pass,
                                         host=db_host, port=db_port)
else:
    raise Exception(f"Unknown db_type in config: {db_type}")


class BaseModel(peewee.Model):
    class Meta:
        database = database


class User(BaseModel):
    username = peewee.CharField(max_length=255, unique=True)
    active_config = peewee.DeferredForeignKey('Config', null=True, backref='+', on_delete='SET_NULL')
    config_sync_token = peewee.CharField(max_length=255, unique=True)
    created_at = peewee.DateTimeField(default=datetime.datetime.utcnow)
    modified_at = peewee.DateTimeField(default=datetime.datetime.utcnow)
    enable = peewee.BooleanField(default=True)

    def save(self, force_insert=False, only=None):
        self.modified_at = datetime.datetime.utcnow()
        return super(User, self).save(force_insert=force_insert, only=only)


class Config(BaseModel):
    user = peewee.ForeignKeyField(User, backref='configs', on_delete='CASCADE')
    name = peewee.CharField(max_length=255)
    content = peewee.TextField(default="{}")
    last_used_with_version = peewee.CharField(max_length=32, null=True)
    created_at = peewee.DateTimeField(default=datetime.datetime.utcnow)
    modified_at = peewee.DateTimeField(default=datetime.datetime.utcnow)

    def save(self, force_insert=False, only=None):
        self.modified_at = datetime.datetime.utcnow()
        return super(Config, self).save(force_insert=force_insert, only=only)


class ConfigHistory(BaseModel):
    config = peewee.ForeignKeyField(Config, on_delete='CASCADE')
    name = peewee.CharField(max_length=255)
    content = peewee.TextField(default="{}")
    last_used_with_version = peewee.CharField(max_length=32, null=True)
    created_at = peewee.DateTimeField()
    modified_at = peewee.DateTimeField(default=datetime.datetime.utcnow)


class ConfigDeleteHistory(BaseModel):
    user = peewee.ForeignKeyField(User, backref='configs', on_delete='CASCADE')
    name = peewee.CharField(max_length=255)
    content = peewee.TextField(default="{}")
    last_used_with_version = peewee.CharField(max_length=32, null=True)
    created_at = peewee.DateTimeField()
    modified_at = peewee.DateTimeField(default=datetime.datetime.utcnow)


User.create_table()
Config.create_table()
ConfigHistory.create_table()
ConfigDeleteHistory.create_table()
