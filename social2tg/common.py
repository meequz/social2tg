import time
from importlib import import_module

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

    def _str(self):
        return f'Update(url={self._url})'

    def __str__(self):
        return self._str()

    def __repr__(self):
        return self._str()

    @property
    def url(self):
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

    def convert(self):
        """
        Convert to the form ready for publishing:
        prepare final text and a list of media
        """
        text = f'{self.author}\n\n{self.text}'
        media = self.media or []
        return text, media


class Post(Update):
    """
    Base class of a Post, in any social source
    """

    def _str(self):
        return f'Post(url={self._url})'


class Media:
    """
    Base class of a Media, in any social source
    """
    def __init__(self, url=None, mtype=None, path=None):
        self.url = url
        self.mtype = mtype
        self.path = path

    def _str(self):
        return f'Media(url={self.url})'

    def __str__(self):
        return self._str()

    def __repr__(self):
        return self._str()


class Image(Media):
    """
    Base class of an Image, in any social source
    """
    def _str(self):
        return f'Image(url={self.url})'


class Video(Media):
    """
    Base class of a Video, in any social source
    """
    def _str(self):
        return f'Video(url={self.url})'


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

    def get_soup(self, url):
        """
        Load URL and returned souped DOM
        """
        self._browser.get(url)
        time.sleep(1)
        return self._browser.get_soup()


class Target:
    """
    Base for any Target class
    """
    def __init__(self, name, id_):
        self.name = name
        self.id = id_

    def publish(self, update):
        raise NotImplementedError

    def schedule(self, update, date):
        raise NotImplementedError


class Feed:

    def __init__(self, name, feed_params):
        """
        Initialize sources and targets of the feed
        """
        self.name = name

        self.sources = []
        logger.info('Create sources: %s', feed_params['sources'])
        for name in feed_params['sources']:
            src = config.SOURCES[name]
            source = import_string(src['class'])(name, src['id'])
            self.sources.append(source)

        self.targets = []
        logger.info('Create targets: %s', feed_params['targets'])
        for name in feed_params['targets']:
            trg = config.TARGETS[name]
            target = import_string(trg['class'])(name, trg['id'])
            self.targets.append(target)

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
                target.publish(update)
                time.sleep(1)


def cleanup():
    """
    Various cleanups at the end of the job
    """
    destroy_browser()
