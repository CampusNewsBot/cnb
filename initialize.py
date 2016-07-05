import rethinkdb as r
import config
import logging


def create_db():
    conn = r.connect(**config.database)
    if 'cnb' in r.db_list().run(conn):
        return

    logging.info('Initializing database')
    r.db_create('cnb').run(conn)
    conn.use('cnb')

    r.table_create('news').run(conn)
    r.table('news').index_create('fetch_date').run(conn)
    r.table_create('bots').run(conn)
    r.table_create('chats').run(conn)

if __name__ == '__main__':
    create_db()
