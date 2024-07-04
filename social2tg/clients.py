import warnings
warnings.filterwarnings('ignore')

import time

import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

import CONFIG
from .constants import HEADERS_LIKE_BROWSER
from .utils import get_logger


_browser = None
_reqclient = None
logger = get_logger()


class Client:

    def get(self):
        raise NotImplementedError

    def scroll_up_down(self):
        pass


class RequestsClient(Client):
    """
    Wrapper on Requests Session
    """
    def __init__(self):
        self._session = requests.session()

        if CONFIG.tor_proxy:
            self._session.proxies['http'] = 'socks5h://localhost:9050'
            self._session.proxies['https'] = 'socks5h://localhost:9050'

    def get(self, url, *args, **kwargs):
        headers = HEADERS_LIKE_BROWSER.copy()
        headers.update(kwargs.get('headers', {}))
        kwargs['headers'] = headers

        if not kwargs.get('verify'):
            kwargs['verify'] = False

        resp = self._session.get(url, *args, **kwargs)
        return resp


class FirefoxBrowser(webdriver.Firefox, Client):
    """
    Wrapper on Selenium driver
    """
    def __init__(self):
        options = Options()
        options.headless = CONFIG.browser_headless

        options.set_preference('permissions.default.image', 2)
        options.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
        options.set_preference('places.history.enabled', False)

        if CONFIG.tor_proxy:
            options.set_preference("network.dns.blockDotOnion", False)
            options.set_preference("network.proxy.type", 1)
            options.set_preference("network.proxy.socks_version", 5)
            options.set_preference("network.proxy.socks", "127.0.0.1")
            options.set_preference("network.proxy.socks_port", 9050)
            options.set_preference("network.proxy.socks_remote_dns", True)

        service = FirefoxService(GeckoDriverManager().install())
        super().__init__(options=options, service=service)

    def __del__(self):
        self.quit()

    def css_select(self, selector):
        try:
            return self.find_element(By.CSS_SELECTOR, selector)
        except NoSuchElementException as e:
            logger.error(str(e))

    def scroll_up_down(self):
        logger.info('Scrolling up and down in the browser')
        self.execute_script('window.scrollTo(0, 0)')
        time.sleep(1)
        self.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(2)


def get_reqclient():
    """
    Return requests client object, creating if necessarry
    """
    global _reqclient
    if _reqclient is None:
        _reqclient = RequestsClient()
    return _reqclient


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
