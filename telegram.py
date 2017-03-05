import json
import logging
import time
import urllib.request
from models import Message
from config import config


class Sender:
    def __init__(self):
        logging.info('Starting Telegram sender')


    def repeat(self):
        while True:
            try:
                self.send_messages()
            except Exception as e:
                send_admin('Exception in message sender: {}'.format(e))
                logging.error(e)

            time.sleep(config()['bot']['send_interval'])

    def send_messages(self):
        logging.info('Sending news')

        if not config()['bot']['enabled']:
            logging.info('Bot is disabled, quitting')
            return

        messages = Message.select().where(Message.send_date == None)

        if len(messages) >= bot['send_limit']:
            error_message =\
                'Too many ({}) messages in send pipeline, disabling bot'\
                .format(sum(self.history))
            logging.error(error_message)
            send_admin(error_message)
            return

        for message in messages:
            channel = list(filter(lambda c: c['channel'] == message.channel,
                            config()['channels']))

            logging.info('Sending news: %s', message['id'])

            if not channel['enabled']:
                logging.info('Channel disabled, not sending')
                continue

            payload = json.dumps(
                {'chat_id': '@' + channel['channel'],
                 'text': '{text}\n-- {author}'.format(message.text, message.author)})

            req = urllib.request.Request(
                url=config()['bot']['url'].format(config['bot']['bot_id']),
                data=payload.encode('utf-8'),
                headers={'Content-Type': 'application/json'})
            resp = urllib.request.urlopen(req)

            if resp.status == 200:
                message.send_date = datetime.datetime.now()
                message.save()
                logging.info('Sent news: %s', message['id'])
            else:
                logging.error('Send failed: %s', message['id'])


def send_admin(message):
    payload = json.dumps(
        {'text': message,
         'chat_id': config()['admin_chat'] })

    req = urllib.request.Request(
        url=config()['bot']['url'].format(config['bot']['bot_id']),
        data=payload.encode('utf-8'),
        headers={'Content-Type': 'application/json'})
    urllib.request.urlopen(req)
