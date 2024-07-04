import datetime
import os
import time

import telegram
from telegram.error import RetryAfter
from telethon.errors.rpcerrorlist import FloodWaitError
from telethon.sync import TelegramClient

from .common import Target
from .utils import get_logger


logger = get_logger()


class TelegramTarget(Target):
    """
    Base for any Telegram target
    """
    caption_limit = 1024
    text_limit = 4096

    def to_target(self, text, footer, media):
        footer = '' if self.params.get('no_footer') else footer

        ending = '...'
        limit = self.caption_limit if media else self.text_limit

        cut = limit - (len(ending) + len(footer))
        if cut < len(text):
            text = text[:cut] + ending

        return text, footer, media


class TelethonChatTarget(TelegramTarget):
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
                time.sleep(exc.seconds + 1)
                action(client, *args)
            time.sleep(2)

    def _publish(self, client, update):
        """
        Action for publishing a post
        """
        text, footer, media = update.to_internal()
        text, footer, media = self.to_target(text, footer, media)
        if text or media:  # TODO: add media
            resp = client.send_message(self.params['chat_id'], text + footer)
            return True

    def publish(self, update):
        logger.info('Publish %s in %s', update, self.name)
        resp = self._tg_exec(self._publish, update)
        return resp


class PtbTarget(TelegramTarget):
    """
    Uses python-telegram-bot lib and Telegram Bot API
    """


class PtbChatTarget(PtbTarget):
    """
    Uses python-telegram-bot lib and Telegram Bot API,
    send update in a chat (channel, group, or user)
    """
    def __init__(self, name, params):
        super().__init__(name, params)
        self.bot = telegram.Bot(token=params['bot_token'])

    def _tg_exec(self, action, *args):
        """
        Execute provided action
        """
        # Clear proxies
        http_proxy, https_proxy = os.environ['http_proxy'], os.environ['https_proxy']
        del os.environ['http_proxy']
        del os.environ['https_proxy']

        resp = None
        try:
            try:
                resp = action(*args)
                time.sleep(2)
            except RetryAfter as exc:
                wait = int(exc.retry_after)
                logger.info('Flood limit detected, waiting for %s seconds', wait)
                time.sleep(wait + 1)
                resp = action(*args)

        except telegram.error.BadRequest as exc:
            logger.error("Fail executing TG action %s: %s", action, exc)

        # Return proxies
        os.environ['http_proxy'], os.environ['https_proxy'] = http_proxy, https_proxy

        return resp

    def _publish(self, text, ptb_media):
        """
        Action for publishing a post
        """
        if ptb_media:
            resp = self.bot.send_media_group(self.params['chat_id'], ptb_media)
        elif text:
            resp = self.bot.send_message(self.params['chat_id'], text, parse_mode='html')
        return resp

    def publish(self, update):
        logger.info('Publish %s in %s', update, self.name)

        text, footer, media = update.to_internal()
        text, footer, media = self.to_target(text, footer, media)

        if text or media:
            text = text + footer

            ptb_media = []
            if media:
                md_0 = media.pop(0)
                ptb_md_0 = md_0.convert_to_ptb(caption=text)
                ptb_media = [ptb_md_0] + [md.convert_to_ptb() for md in media]

            resp = self._tg_exec(self._publish, text, ptb_media)
            return True


class PtbBotTarget(PtbTarget):
    """
    Uses python-telegram-bot lib and Telegram Bot API,
    send update to all the bot subscribers
    """
