from logging import getLogger
from time import sleep

import peewee

import config
from common.db import basic
from common.models import db_models

log = getLogger(__name__)

tables = [
    db_models.Project,
    db_models.User,
    db_models.ProjectToUser,
    db_models.LastKnownState,
]


def start(max_connections=10):
    for i in range(10):
        try:
            basic.pg_db.init(
                database=config.DB_NAME,
                user=config.DB_USER,
                password=config.DB_PASS,
                host=config.DB_HOST,
                port=config.DB_PORT,
                max_connections=max_connections,
            )
            basic.pg_db.connect()
        except peewee.OperationalError:
            if i == 9:
                raise
            log.info('DB unavailable')
            sleep(1)
            continue
        else:
            break
    create_tables()

    return basic.manager


def create_tables():
    for table in tables:
        table.create_table()
