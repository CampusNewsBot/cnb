import json
import time
import logging
import urllib.request
import rethinkdb as r
import config


class Sender:
    def __init__(self):
        logging.info('Starting Telegram sender')
        self.db = r.connect(host=config.database['host'],
                            db=config.database['name'])

    def send_messages(self):
        for message in r.table('news').filter({'send_date': None})\
                .run(self.db):
            bot_id = r.table('bots').get('cnb').run(self.db)['bot_id']
            chat_id = r.table('chats').get(message['chat'])\
                .run(self.db)['chat_id']
            payload = json.dumps({'chat_id': '@' + chat_id,
                                  'text': message['text']})

            status = None
            while status != 200:
                logging.info('Sending news %s', message['id'])
                req = urllib.request.Request(
                    url=config.telegram_url.format(bot_id),
                    data=payload.encode('utf-8'),
                    headers={'Content-Type': 'application/json'})

                if config.DEBUG and config.DEBUG_NO_SEND:
                    return

                resp = urllib.request.urlopen(req)
                status = resp.status

                if status == 200:
                    r.table('news').get(message['id'])\
                        .update({'send_date': r.now()}).run(self.db)
                else:
                    logging.error('Send failed %s', message['id'])
                    time.sleep(10)
