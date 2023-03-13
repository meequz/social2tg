import random
import time
from importlib import import_module

from bs4 import BeautifulSoup
from telegram import InputMediaPhoto, InputMediaVideo

import config
from .clients import destroy_browser, get_browser, get_reqclient
from .utils import get_logger, import_string


logger = get_logger()


class Update:
    """
    Base class of an Update, in any social source.
    Update is any update entity such as post, story, etc
    """
    _url = None
    _author = None
    _date = None
    _text = None
    _media = None
    orig_url = None
    update_type = None

    def __init__(self, params):
        self.params = params

    def _str(self):
        return f"Update('{self._url}')"

    def __str__(self):
        return self._str()

    def __repr__(self):
        return self._str()

    @property
    def url(self):
        return self._url

    @property
    def identifier(self):
        return self._url

    @property
    def author(self):
        return self._author or ''

    @property
    def date(self):
        return self._date

    @property
    def text(self):
        return self._text or ''

    @property
    def media(self):
        return self._media

    def construct_footer(self):
        update_type = self.update_type.title()

        if self.orig_url:
            start = f'<a href="{self.orig_url}">{update_type}</a>'
        else:
            start = update_type

        footer = f'\n\n<i>{start} by <code>{self.author}</code></i>'
        return footer

    def to_internal(self):
        """
        Convert to the form ready for publishing:
        prepare final text and a list of media
        """
        text = self.text.strip()
        footer = self.construct_footer()
        media = self.media or []
        return text, footer, media


class Post(Update):
    """
    Base class of a Post, in any social source
    """
    update_type = 'post'

    def _str(self):
        return f"Post('{self._url}')"


class Media:
    """
    Base class of a Media, in any social source
    """
    def __init__(self, url=None, mtype=None, path=None):
        self.url = url
        self.mtype = mtype
        self.path = path

    def _str(self):
        return f"Media('{self.url}')"

    def __str__(self):
        return self._str()

    def __repr__(self):
        return self._str()


class Image(Media):
    """
    Base class of an Image, in any social source
    """
    def _str(self):
        return f"Image('{self.url}')"

    def convert_to_ptb(self, caption=''):
        """
        Convert to python-telegram-bot object
        """
        return InputMediaPhoto(self.url, caption=caption, parse_mode='html')


class Video(Media):
    """
    Base class of a Video, in any social source
    """
    def _str(self):
        return f"Video('{self.url}')"

    def convert_to_ptb(self, caption=''):
        """
        Convert to python-telegram-bot object
        """
        return InputMediaVideo(self.url, caption=caption, parse_mode='html')


class Source:
    """
    Base for any Source class
    """
    RETRIES = 3
    last_resp_text = ''

    def __init__(self, name, params):
        self.name = name
        self.params = params

    def open(self, url):
        """
        Load URL, and wait a bit for JS to load
        """
        ok = False
        retry = 0
        while retry < self.RETRIES:
            try:
                self.last_resp_text = self.http_get(url)
                ok = True
                break
            except Exception as exc:
                logger.error('Retrying because of error: %s', str(exc).strip())
                retry += 1
                time.sleep(retry * 4)

        if ok:
            time.sleep(config.WAIT_BETWEEN)
        else:
            raise ValueError('Enough retries! Give it a rest')

    def get_soup(self):
        """
        Return the souped DOM
        """
        return BeautifulSoup(self.last_resp_text, 'html.parser')

    def get_updates(self):
        raise NotImplementedError


class SeleniumSource(Source):
    """
    Mixin for any Source working with Selenium
    """
    def init_session(self):
        self._client = get_browser()

    def http_get(self, url):
        """
        Just simply get, without retries or smth
        """
        logger.info('selenium.get: %s', url)
        self._client.get(url)
        return self._client.page_source


class RequestsSource(Source):
    """
    Mixin for any Source working with Requests
    """
    def init_session(self):
        self._client = get_reqclient()

    def http_get(self, url):
        """
        Just simply get, without retries or smth
        """
        logger.info('requests.get: %s', url)
        response = self._client.get(url)
        if response.status_code > 399:
            raise ValueError(f'Got {response.status_code} status code')
        return response.text


class DummyPost(Post):
    """
    Fake Post for testing
    """
    _text = f'Lorem ipsum {random.randint(1, 99999999999)}'


class DummySource(Source):
    """
    Fake Source for testing
    """
    def get_updates(self):
        posts = [DummyPost({'id': '1'})]
        return posts


class Target:
    """
    Base for any Target class
    """
    def __init__(self, name, params):
        self.name = name
        self.params = params

    def _str(self):
        return f"Target('{self.name}')"

    def publish(self, update):
        raise NotImplementedError

    def schedule(self, update, date):
        raise NotImplementedError


class DummyTarget(Target):
    """
    Fake Telegram channel target, for testing
    """
    def publish(self, update):
        text, footer, media = update.to_internal()
        print(f'{update} published in {self.name}:')
        print(f'{text=}')
        print(f'{footer=}')
        print(f'{media=}')
        print()

        return True


class Feed:
    """
    Feed is [sources] -> [targets] system
    """
    _storage = None

    def __init__(self, name, params):
        """
        Initialize sources and targets of the feed
        """
        self.name = name
        self.params = params
        logger.info('Processing %s: %s > %s', self, params['sources'], params['targets'])

        self.sources = []
        for name in params['sources']:
            src = config.SOURCES[name]
            source = import_string(src['class'])(name, src)
            self.sources.append(source)

        self.targets = []
        for name in params['targets']:
            trg = config.TARGETS[name]
            target = import_string(trg['class'])(name, trg)
            self.targets.append(target)

    def _str(self):
        return f"Feed('{self.name}')"

    def __str__(self):
        return self._str()

    def __repr__(self):
        return self._str()

    @property
    def storage(self):
        if self._storage is None:
            self._storage = import_string(self.params['storage']['class'])(self.params['storage'])
        return self._storage

    def gather(self):
        """
        Gather all updates from all the feed's sources
        """
        updates = []
        for src in self.sources:
            src_updates = src.get_updates()
            updates.extend(src_updates)
        return updates

    def publish(self, updates):
        """
        Publish all the gathered updates to all the feed's targets
        """
        for target in self.targets:
            for update in updates:

                if self.storage.find_published(update, self):
                    logger.info('%s for %s already published', update, self)
                    continue

                if published := target.publish(update):
                    logger.info('Remember: %s published in %s', update, self)
                    self.storage.remember_published(update, self)
                else:
                    logger.error('Error, %s not published in %s', update, target)


def cleanup():
    """
    Various cleanups at the end of the job
    """
    destroy_browser()
