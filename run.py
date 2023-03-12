import os
import time

import config
from social2tg.common import Feed, cleanup
from social2tg.utils import get_logger


logger = get_logger()


def restart_tor():
    logger.info('Restarting Tor')
    os.system('sudo systemctl restart tor')
    time.sleep(10)


def process_feed(name):
    feed_params = config.FEEDS[name]
    feed = Feed(name, feed_params)
    updates = feed.gather()
    feed.publish(updates)
    time.sleep(config.BETWEEN_SOURCES_DELAY)


def main():
    """
    Gather updates and publish it for each Feed from settings
    """
    if config.TOR_PROXY:
        restart_tor()

    for feed_name in config.FEEDS:
        process_feed(feed_name)

    cleanup()


if __name__ == '__main__':
    main()
