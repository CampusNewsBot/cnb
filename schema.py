import datetime
import logging
from peewee import *
from config import config

db = PostgresqlDatabase(config['database']['database'],
                        host=config['database']['host'],
                        port=config['database']['port'],
                        user=config['database']['user'],
                        password=config['database']['password'])


class Department(Model):
    name = CharField()

    class Meta:
        database = db

class Author(Model):
    department = ForeignKeyField(Department, related_name='authors')
    name = CharField()

    class Meta:
        database = db

class Message(Model):
    date = DateTimeField(default=datetime.datetime.now)
    author = ForeignKeyField(Author, related_name='messages')
    text = TextField()
    receivers = IntegerField(default=-1)

    class Meta:
        database = db

def tables_creator():
    db.connect()
    tables = [Department,Author,Message]
    for table in reversed(tables):
        if table.table_exists():
            logging.debug('DroppingTable', extra={'table':table})
            table.drop_table()
    for table in tables:
        logging.debug('CreatingTable', extra={'table':table})
        table.create_table()

    db.close()
