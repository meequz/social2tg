import time

import config
from social2tg.common import Feed, cleanup


def main():
    """
    Gather updates and publish it for each Feed from settings
    """
    for feed_name in config.FEEDS:
        feed_params = config.FEEDS[feed_name]
        feed = Feed(feed_name, feed_params)
        updates = feed.gather()
        feed.publish(updates)

        time.sleep(1)

    cleanup()


if __name__ == '__main__':
    main()
