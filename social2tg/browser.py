import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

import config
from .utils import get_logger


_browser = None
logger = get_logger()


class FirefoxBrowser(webdriver.Firefox):
    """
    Wrapper on Selenium driver
    """
    def __init__(self):
        options = Options()
        options.headless = config.BROWSER_HEADLESS

        options.set_preference('permissions.default.image', 2)
        options.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
        options.set_preference('network.dns.blockDotOnion', False)
        options.set_preference('places.history.enabled', False)

        service = FirefoxService(GeckoDriverManager().install())
        super().__init__(options=options, service=service)

    def __del__(self):
        self.quit()

    def get(self, url):
        logger.info('Open in browser: %s', url)
        result = super().get(url)
        return result

    def get_soup(self):
        """
        Using Beautiful Soup for parsing is easier than Selenium.
        """
        return BeautifulSoup(self.page_source, "html.parser")

    def css_select(self, selector):
        try:
            return self.find_element(By.CSS_SELECTOR, selector)
        except NoSuchElementException as e:
            logging.error(str(e))

    def scroll_up_down(self):
        self.execute_script('window.scrollTo(0, 0)')
        time.sleep(1)
        self.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(2)


def get_browser():
    """
    Return Selenium driver object, creating if necessarry
    """
    global _browser
    if _browser is None:
        _browser = FirefoxBrowser()
    return _browser


def destroy_browser():
    if _browser is not None:
        _browser.quit()
