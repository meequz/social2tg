from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import config


_browser = None


class FirefoxBrowser(webdriver.Firefox):

    def __init__(self):
        options = Options()
        options.headless = config.BROWSER_HEADLESS

        options.set_preference('permissions.default.image', 2)
        options.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
        options.set_preference('network.dns.blockDotOnion', False)
        options.set_preference('places.history.enabled', False)

        super().__init__(options=options)

    def get_soup(self):
        return BeautifulSoup(self.page_source, 'html.parser')

    def scroll_up_down(self):
        self.execute_script('window.scrollTo(0, 0)')
        time.sleep(1)
        self.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(2)


def get_browser():
    """
    Get the browser, creating if necessarry
    """
    global _browser
    if _browser is None:
        _browser = FirefoxBrowser()
    return _browser


def destroy_browser():
    if _browser is not None:
        _browser.quit()
