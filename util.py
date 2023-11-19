import datetime
import secrets


def generate_token(length=128):
    random_bytes = secrets.token_bytes(int(length / 2) + 1)
    return random_bytes.hex()[0:length]


def format_timestamp(dt):
    if not isinstance(dt, datetime.datetime):
        dt = datetime.datetime.fromtimestamp(dt / 1000.0)
    return dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')


def format_config_dict(d):
    d['user'] = d['user']['id']
    d['created_at'] = format_timestamp(d['created_at'])
    d['modified_at'] = format_timestamp(d['modified_at'])
    return d
