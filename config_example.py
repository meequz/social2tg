from datetime import timedelta
from pathlib import Path

from social2tg.base_config import *


TARGETS = {
    # name: {
    #     'chat_id': -1,
    #     'class': 'social2tg.tg.PtbChatTarget',
    #     'bot_token': '',
    # },
    # name: {
    #     'chat_id': -2,
    #     'class': 'social2tg.tg.TelethonChatTarget',
    #     'api_id': 0,
    #     'api_hash': '',
    #     'session': '',
    # },
}

SOURCES = {
    # name: {
    #     'class': 'social2tg.inst.GramhirSeleniumSource',
    #     'id': nickname,
    # }
}

FEEDS = {
    # name: {
    #     'sources': [source_name_1, source_name_2, ...],
    #     'targets': [target_name, ...],
    # },
}
