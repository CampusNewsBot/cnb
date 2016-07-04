import rethinkdb as r
import config


def create_db():
    conn = r.connect(host=config.database['host'], db=config.database['name'])
    if 'cnb' in r.db_list().run(conn):
        return

    r.db_create('cnb').run(conn)
    conn.use('cnb')

    r.table_create('news').run(conn)
    r.table('news').index_create('fetch_date').run(conn)
    r.table_create('bots').run(conn)
    r.table_create('chats').run(conn)

if __name__ == '__main__':
    create_db()
