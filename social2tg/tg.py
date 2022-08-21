import time
import datetime

from telethon.errors.rpcerrorlist import FloodWaitError
from telethon.sync import TelegramClient

import config
from .common import Target
from .utils import get_logger


logger = get_logger()


class BaseTarget(Target):

    def _tg_exec(self, action, *args):
        """
        Execute provided action with provided args
        """
        with TelegramClient(config.TG_SESSION_NAME,
                            config.TG_API_ID,
                            config.TG_API_HASH) as client:
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
        resp = client.send_message(self.id, text)
        return resp

    def publish(self, update):
        logger.info('Publish %s in %s', update, self.name)
        resp = self._tg_exec(self._publish, update)
        return resp


class ChannelTarget(BaseTarget):
    """
    Use this class if your target is a Telegram channel
    """


class DummyChannelTarget(BaseTarget):
    """
    Fake Telegram channel target, for testing
    """
    def publish(self, update):
        text, media = update.convert()
        print(f'{update} published in {self.name}:')
        print(f'{text=}')
        print(f'{media=}')
        print()
