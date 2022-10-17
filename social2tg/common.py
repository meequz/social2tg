import time
from importlib import import_module

from telegram import InputMediaPhoto, InputMediaVideo

import config
from .browser import destroy_browser, get_browser
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

    def _str(self):
        return f"Update(url='{self._url}')"

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
        return self._author

    @property
    def date(self):
        return self._date

    @property
    def text(self):
        return self._text

    @property
    def media(self):
        return self._media

    @property
    def footer(self):
        footer = (
            f'\n\n<i><a href="{self.orig_url}">{self.update_type.title()}</a> '
            f'by <code>{self.author}</code></i>'
        )
        return footer

    def convert_to_internal(self):
        """
        Convert to the form ready for publishing:
        prepare final text and a list of media
        """
        text = f'{self.text.strip()}{self.footer}'
        media = self.media or []
        return text, media


class Post(Update):
    """
    Base class of a Post, in any social source
    """
    update_type = 'post'

    def _str(self):
        return f"Post(url='{self._url}')"


class Media:
    """
    Base class of a Media, in any social source
    """
    def __init__(self, url=None, mtype=None, path=None):
        self.url = url
        self.mtype = mtype
        self.path = path

    def _str(self):
        return f"Media(url='{self.url}')"

    def __str__(self):
        return self._str()

    def __repr__(self):
        return self._str()


class Image(Media):
    """
    Base class of an Image, in any social source
    """
    def _str(self):
        return f"Image(url='{self.url}')"

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
        return f"Video(url='{self.url}')"

    def convert_to_ptb(self, caption=''):
        """
        Convert to python-telegram-bot object
        """
        return InputMediaVideo(self.url, caption=caption, parse_mode='html')


class Source:
    """
    Base for any Source class
    """
    def get_updates(self):
        raise NotImplementedError


class SeleniumSource(Source):
    """
    Mixin for any class working with Selenium
    """
    def _create_browser(self):
        self._browser = get_browser()

    def get_soup(self, url, wait=2):
        """
        Load URL, wait a bit for JS to load, and return the souped DOM
        """
        self._browser.get(url)
        time.sleep(wait)
        return self._browser.get_soup()


class Target:
    """
    Base for any Target class
    """
    def __init__(self, name, params):
        self.name = name
        self.params = params

    def publish(self, update):
        raise NotImplementedError

    def schedule(self, update, date):
        raise NotImplementedError


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

        self.sources = []
        logger.info('Create sources: %s', params['sources'])
        for name in params['sources']:
            src = config.SOURCES[name]
            source = import_string(src['class'])(name, src['id'])
            self.sources.append(source)

        self.targets = []
        logger.info('Create targets: %s', params['targets'])
        for name in params['targets']:
            trg = config.TARGETS[name]
            target = import_string(trg['class'])(name, trg)
            self.targets.append(target)

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
            updates.extend(src.get_updates())
        return updates

    def publish(self, updates):
        """
        Publish all the gathered updates to all the feed's targets
        """
        for target in self.targets:
            for update in updates:
                if self.storage.find_published(update, self):
                   continue
                target.publish(update)
                self.storage.remember_published(update, self)
                time.sleep(1)


def cleanup():
    """
    Various cleanups at the end of the job
    """
    destroy_browser()
