import os
import time

import config
from social2tg.common import Feed, cleanup


def restart_tor():
    os.system('sudo systemctl restart tor')
    time.sleep(10)


def process_feed(name):
    feed_params = config.FEEDS[name]
    feed = Feed(name, feed_params)
    updates = feed.gather()
    feed.publish(updates)
    time.sleep(1)


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
