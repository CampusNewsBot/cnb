import sys
import datetime
import requests
import pytz

date = datetime.datetime.now()
tz = pytz.timezone('Europe/Rome')
date = tz.localize(date)

try:
    with open('message.txt') as f:
        MESSAGE = f.read()
except:
    print('Create a message.txt with your message')

BASE_URL= 'https://api.telegram.org/{}/sendMessage'
channels = [
  {'name': 'disi', 'channel': 'UnitnDisiNews', 'bot_key': 'uxFqniRPvgZSHM5aCfHkFBZ3AK0V1LdSwV2EIfTDzR7oCt8y'},
  {'name': 'diicibio', 'channel': 'UnitnDiiCibioNews', 'bot_key': '8w6aTfCSGspWDqhdfSpImumrPrM7E9QbhfLIKa0nNri1gruq'},
  {'name': 'dicam', 'channel': 'UnitnDicamNews', 'bot_key': 'qoqRBTMxLGlQJkM5pskaYwy9hwFH53fk3tOIudMTrVyGkZKT'},
  {'name': 'lettere', 'channel': 'UnitnLettereNews', 'bot_key': 'kyw2V345lCdXgRI3uKTXTbyCdT6tsSr5YqgEoe0tduioux5i'},
  {'name': 'giurisprudenza', 'channel': 'UnitnGiuriNews', 'bot_key': 'lR7IUd1T6ELdLchJWLz6gswqrZxmsoQgupd4xHs2pkF630QZ'},
  {'name': 'economia', 'channel': 'UnitnEconomiaNews', 'bot_key': '6h2fJKPFX4iWWSuq5xAbBcc3k09WrZHHm1fL9Xnx7U0hfd19'},
  {'name': 'sociologia', 'channel': 'UnitnSociologiaNews', 'bot_key': 'ytTHTtH2UsTcu9otlu3ssBxOoWa1wGWv1GBsm8Y2kdqVVvKD'},
  {'name': 'cogsci', 'channel': 'UnitnCogsciNews', 'bot_key': 'HSIFAMXqoHKCTFqjLZwKWbNwGKy5smE3SQeKMC5N7pNSTN6u'}
]

print(MESSAGE)
ask = input("Do you really want to send this message to all channels? [y/N]")

if 'y' not in ask:
    sys.exit(1)

for channel in channels:
    url = BASE_URL.format(channel['name'])
    headers = {'X-Auth-Key': channel['bot_key']}
    payload = {'author': 'Bot admins', 'date': date.isoformat('T'),
               'text': BASE_MESSAGE.format(channel['channel'])}
    response = requests.post(url=url, json=payload, headers=headers)
    print(channel['name'], response.status_code, payload, headers, url, '\n\n')
