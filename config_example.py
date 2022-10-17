from datetime import timedelta
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
BROWSER_HEADLESS = True


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
    #     'class': 'social2tg.inst.GramhirSource',
    #     'id': nickname,
    # }
}

FEEDS = {
    # name: {
    #     'sources': [source_name_1, source_name_2, ...],
    #     'targets': [target_name, ...],
    # },
}
