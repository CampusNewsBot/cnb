import json
import logging
import time
import urllib.request
import rethinkdb as r
import config

BOT_QUERY = r.table('bots').get('cnb')


class Sender:
    def __init__(self):
        logging.info('Starting Telegram sender')
        self.db = r.connect(**config.database)

    def repeat(self):
        while True:
            try:
                self.send_messages()
            except Exception as e:
                send_admin('Exception in message sender: {}'.format(e))
                logging.error(e)
            bot = BOT_QUERY.run(self.db)
            time.sleep(bot['send_interval'])

    def send_messages(self):
        logging.info('Sending news')
        bot = BOT_QUERY.run(self.db)

        if not bot['enabled'] or config.DEBUG_NO_SEND:
            logging.info('Bot is disabled, quitting')
            return

        messages = list(
            r.table('news').filter({'send_date': None}).run(self.db))

        if len(messages) >= bot['send_limit']:
            BOT_QUERY.update({'enabled': False}).run(self.db)
            error_message =\
                'Too many ({}) messages in send pipeline, disabling bot'\
                .format(sum(self.history))
            logging.error(error_message)
            send_admin(error_message)
            return

        chats = r.table('chats').run(self.db)
        for message in messages:
            chat = [x for x in chats if x['id'] == message['chat']][0]

            logging.info('Sending news: %s', message['id'])

            if not chat and chat['enabled']:
                logging.info('Chat disabled, not sending')
                continue

            payload = json.dumps(
                {'chat_id': '@' + chat['chat_id'],
                 'text': '{text}\n-- {author}'.format(**message)})

            req = urllib.request.Request(
                url=config.telegram_url.format(bot['bot_id']),
                data=payload.encode('utf-8'),
                headers={'Content-Type': 'application/json'})
            resp = urllib.request.urlopen(req)

            if resp.status == 200:
                r.table('news').get(message['id'])\
                    .update({'send_date': r.now()}).run(self.db)
                logging.info('Sent news: %s', message['id'])
            else:
                logging.error('Send failed: %s', message['id'])


def send_admin(message):
    db = r.connect(**config.database)
    payload = json.dumps(
        {'text': message,
         'chat_id': r.table('chats').get('admin').run(db)['chat_id']})

    req = urllib.request.Request(
        url=config.telegram_url.format(BOT_QUERY.run(db)['bot_id']),
        data=payload.encode('utf-8'),
        headers={'Content-Type': 'application/json'})
    urllib.request.urlopen(req)
