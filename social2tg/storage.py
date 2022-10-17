import datetime

import config


class Storage:
    """
    Base for any storage class
    """
    def __init__(self, params):
        raise NotImplementedError

    def remember_published(self, update, feed):
        raise NotImplementedError

    def find_published(self, update, feed):
        raise NotImplementedError


class MemoryStorage:
    """
    In-memory storage. Suitable only for temporary testing usage
    """
    def __init__(self, params):
        self.mem = {
            'published': [],
        }

    def remember_published(self, update, feed):
        now = datetime.datetime.utcnow()
        entry = {'update': update.identifier, 'feed': feed.name, 'at': now}
        self.mem['published'].append(entry)

    def find_published(self, update, feed):
        for entry in self.mem['published']:
            update_found = entry['update'] == update.identifier
            feed_found = entry['feed'] == feed.name
            if update_found and feed_found:
                return entry
