import json
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
            bot = r.table('bots').get('cnb').run(self.db)
            chat = r.table('chats').get(message['chat']).run(self.db)
            if not (bot and bot['enabled'] and chat and chat['enabled']) or\
                    (config.DEBUG and config.DEBUG_NO_SEND):
                continue
            bot_id = bot['bot_id']
            chat_id = chat['chat_id']

            payload = json.dumps({'chat_id': '@' + chat_id,
                                  'text': message['text']})

            logging.info('Sending news %s', message['id'])
            req = urllib.request.Request(
                url=config.telegram_url.format(bot_id),
                data=payload.encode('utf-8'),
                headers={'Content-Type': 'application/json'})
            resp = urllib.request.urlopen(req)

            if resp.status == 200:
                r.table('news').get(message['id'])\
                    .update({'send_date': r.now()}).run(self.db)
            else:
                logging.error('Send failed %s', message['id'])
