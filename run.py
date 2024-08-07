import os
import ssl
import time

import CONFIG
from social2tg.common import Feed, cleanup
from social2tg.utils import get_logger


logger = get_logger()


def handle_connection():
    if CONFIG.disable_ssl:
        ssl.SSLContext.verify_mode = property(
            lambda self: ssl.CERT_NONE, lambda self, newval: None)

    if CONFIG.tor_proxy:
        os.environ['http_proxy'] = 'socks5h://localhost:9050'
        os.environ['https_proxy'] = 'socks5h://localhost:9050'

        logger.info('Restarting Tor')
        os.system('sudo systemctl restart tor')
        time.sleep(10)

    elif CONFIG.proxy:
        os.environ['http_proxy'] = CONFIG.proxy
        os.environ['https_proxy'] = CONFIG.proxy


def process_feed(name):
    feed_params = CONFIG.feeds[name]
    feed = Feed(name, feed_params)
    updates = feed.gather()
    feed.publish(updates)
    time.sleep(CONFIG.delay_after_source)


def main():
    """
    Gather updates and publish it for each Feed from settings
    """
    handle_connection()

    for feed_name in CONFIG.feeds:
        process_feed(feed_name)

    cleanup()


if __name__ == '__main__':
    main()
