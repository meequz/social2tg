from datetime import timedelta
from pathlib import Path

from social2tg.base_config import *


targets = {
    'source_name_1': {
        'chat_id': -1,
        'class': 'social2tg.tg.PtbChatTarget',
        'bot_token': '',
    },
    'source_name_2': {
        'chat_id': -2,
        'class': 'social2tg.tg.TelethonChatTarget',
        'api_id': 0,
        'api_hash': '',
        'session': '',
    },
}

sources = {
    'target_name': {
        'class': 'social2tg.inst.GramhirSeleniumSource',
        'id': 'nickname',
    }
}

feeds = {
    'feed_name': {
        'sources': ['source_name_1', 'source_name_2', ...],
        'targets': ['target_name', ...],
    },
}
