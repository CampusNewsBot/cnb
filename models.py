from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
import datetime
import logging
import config

db = SqliteExtDatabase(config.config()['db_path'])

class BaseModel(Model):
    class Meta:
        database = db


class Message(BaseModel):
    text = TextField()
    author = TextField()
    message_id = TextField()
    channel = TextField()
    fetch_date = DateTimeField(default=datetime.datetime.now)
    send_date = DateTimeField(null=True)


def init_db():
    db.connect()
    for table in [Message]:
        if not table.table_exists():
        logging.info('Initializing database')
        db.create_table(table)
