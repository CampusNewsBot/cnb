#!/usr/bin/env python3
import json
import urllib.request

BOT_ID = '237491003:AAGLcRsBfDSOpSRzqAFl-M8KcCuuVL4MJwU'
URL = 'https://api.telegram.org/bot{}/getChatMembersCount'.format(BOT_ID)
CHANNELS = ['UnitnDisiNews', 'UnitnDiiCibioNews', 'UnitnDicamNews',
            'UnitnLettereNews', 'UnitnGiuriNews', 'UnitnEconomiaNews',
            'UnitnSociologiaNews', 'UnitnCogsciNews']


def get_count(handle):
    payload = {'chat_id': handle}
    req = urllib.request.Request(
        url=URL, data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'})
    resp = urllib.request.urlopen(req)
    return json.loads(str(resp.read(), 'utf-8'))['result']

counts = {channel: get_count('@' + channel) for channel in CHANNELS}
print(counts)
print('TOTAL: {}'.format(sum(counts.values())))
print('Percentage of bot users:', int(sum(counts.values()) / 1990 * 100))
