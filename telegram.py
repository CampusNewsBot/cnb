import json
import time
import logging
import urllib.request
import rethinkdb as r
import config


def send_messages():
    logging.info('Starting Telegram sender')
    TELEGRAM_URL = 'https://api.telegram.org/bot{}/sendMessage'

    conn = r.connect(host=config.database['host'], db=config.database['name'])
    feed = r.table('news').filter({'sent': False}).changes().run(conn)

    for change in feed:
        bot_id = r.table('bots').get('cnb').run(conn)['bot_id']
        chat_id = r.table('chats').get(change['chat']).run(conn)['chat_id']
        payload = json.dumps({'chat_id': chat_id, 'text': change['text']})

        status = None
        while status != 200:
            logging.info('Sending news', change['id'])
            req = urllib.request.Request(url=TELEGRAM_URL.format(bot_id),
                                         data=payload,
                                         headers={'Content-Type':
                                         'application/json'})

            if config.DEBUG and config.DEBUG_NO_SEND:
                return

            resp = urllib.request.urlopen(req)
            status = resp.status

            if status == 200:
                change['sent'] = True
            else:
                logging.error('Send failed', change['id'])
                time.sleep(10)
