import sqlite3
import time
from contextlib import contextmanager

import config


class Storage:
    """
    Base for any storage class
    """
    def __init__(self, params):
        self.params = params

    def remember_published(self, update, feed):
        raise NotImplementedError

    def find_published(self, update, feed):
        raise NotImplementedError


class MemoryStorage(Storage):
    """
    In-memory storage. Suitable only for temporary testing usage
    """
    def __init__(self, params):
        super().__init__(params)
        self.mem = {
            'published': [],
        }

    def remember_published(self, update, feed):
        entry = {
            'update_id': update.identifier,
            'feed': feed.name,
            'at': time.time(),
        }
        self.mem['published'].append(entry)

    def find_published(self, update, feed):
        for entry in self.mem['published']:
            update_found = entry['update_id'] == update.identifier
            feed_found = entry['feed'] == feed.name
            if update_found and feed_found:
                return entry


class SqliteStorage(Storage):

    def __init__(self, params):
        super().__init__(params)
        self.path = params['path']

        sql = 'CREATE TABLE IF NOT EXISTS published (update_id text, feed text, at integer)'
        with get_sqlite_cursor(self.path) as cursor:
            cursor.execute(sql, params)

    def remember_published(self, update, feed):
        sql = 'INSERT INTO published (update_id, feed, at) VALUES (?, ?, ?)'
        params = (update.identifier, feed.name, time.time())
        with get_sqlite_cursor(self.path) as cursor:
            cursor.execute(sql, params)

    def find_published(self, update, feed):
        sql = 'SELECT * FROM published WHERE update_id = ? AND feed = ?'
        params = (update.identifier, feed.name)
        with get_sqlite_cursor(self.path) as cursor:
            cursor.execute(sql, params)
            result = cursor.fetchone()
        return result


@contextmanager
def get_sqlite_cursor(path):
    """
    Emulate context manager since Sqlite lib doesn't have it
    """
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    yield cursor
    conn.commit()
    conn.close()
