import logging
import json

def config(path="channels.json"):
    with open(path, 'r') as f:
        c = json.loads(f.read())
    c['log_level'] = logging.DEBUG if c['log']['level'] == 'debug' else logging.INFO
    return c
