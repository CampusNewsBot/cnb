import json
import logging
import time
import collections
import urllib.request
import rethinkdb as r
import config


class Sender:
    def __init__(self):
        logging.info('Starting Telegram sender')
        self.db = r.connect(**config.database)
        self.history = collections.deque(maxlen=config.send_limit_intervals)

    def repeat(self):
        while True:
            self.send_messages()
            time.sleep(config.send_timeout)

    def send_messages(self):
        bot = r.table('bots').get('cnb').run(self.db)
        if not (bot and bot['enabled']) or\
                (config.DEBUG and config.DEBUG_NO_SEND):
            return

        messages = r.table('news').filter({'send_date': None}).run(self.db)
        self.history.append(len(messages))

        if sum(self.history) >= config.send_limit_messages:
            r.table('bots').get('cnb').update({'enabled': False}).run(self.db)
            error_message =\
                'Too many ({}) messages in send pipeline, disabling bot'\
                .format(config.max_messages_per_interval)
            logging.error(error_message)
            send_admin(error_message)
            return

        for message in messages:
            chat = r.table('chats').get(message['chat']).run(self.db)
            if not chat and chat['enabled']:
                continue
            bot_id = bot['bot_id']
            chat_id = chat['chat_id']

            payload = json.dumps(
                {'chat_id': '@' + chat_id,
                 'text': '{text}\n-- {author}'.format(**message)})

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


def send_admin(message):
    db = r.connect(**config.database)
    bot_id = r.table('bots').get('cnb').run(db)['bot_id']
    payload = json.dumps({'chat_id': r.table('chats').get('admin').run(db),
                          'text': message})

    req = urllib.request.Request(
        url=config.telegram_url.format(bot_id),
        data=payload.encode('utf-8'),
        headers={'Content-Type': 'application/json'})
    urllib.request.urlopen(req)
