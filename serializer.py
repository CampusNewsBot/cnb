import datetime
import pytz
from config import config

def date_serializer(obj):
    """Date JSON serializer."""
    if isinstance(obj, datetime.datetime):
        tz = pytz.timezone(config['timezone'])
        obj = tz.localize(obj)
        obj = obj.replace(second=0, microsecond=0)
        return obj.isoformat('T')
