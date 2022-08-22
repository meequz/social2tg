import time
import datetime

from telethon.errors.rpcerrorlist import FloodWaitError
from telethon.sync import TelegramClient

from .common import Target
from .utils import get_logger


logger = get_logger()


class TelethonChatTarget(Target):
    """
    Uses Telethon lib and Telegram Core API
    """
    def _tg_exec(self, action, *args):
        """
        Execute provided action with provided args
        """
        with TelegramClient(self.params['session'],
                            self.params['api_id'],
                            self.params['api_hash']) as client:
            try:
                action(client, *args)
            except FloodWaitError as exc:
                wait_time = datetime.timedelta(seconds=exc.seconds)
                time.sleep(exc.seconds + 1)
                action(client, *args)
            time.sleep(2)

    def _publish(self, client, update):
        """
        Action for publishing a post
        """
        text, media = update.convert()
        resp = client.send_message(self.params['chat_id'], text)
        return resp

    def publish(self, update):
        logger.info('Publish %s in %s', update, self.name)
        resp = self._tg_exec(self._publish, update)
        return resp


class PtbTarget(Target):
    """
    Uses python-telegram-bot lib and Telegram Bot API
    """


class PtbChatTarget(Target):
    """
    Uses python-telegram-bot lib and Telegram Bot API,
    send update in a chat (channel, group, or user)
    """


class PtbBotTarget(Target):
    """
    Uses python-telegram-bot lib and Telegram Bot API,
    send update to all the bot subscribers
    """


class DummyTarget(Target):
    """
    Fake Telegram channel target, for testing
    """
    def publish(self, update):
        text, media = update.convert()
        print(f'{update} published in {self.name}:')
        print(f'{text=}')
        print(f'{media=}')
        print()
