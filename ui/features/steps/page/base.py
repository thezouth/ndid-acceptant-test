from abc import ABC, abstractmethod
from typing import Optional

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

def open_browser() -> WebDriver:
    return webdriver.Chrome()


class PageObject(ABC):
    def __init__(self, browser: Optional[WebDriver] = None):
        self._browser = browser if browser else open_browser()

    def _wait(self, timeout=3) -> WebDriverWait:
        return WebDriverWait(self._browser, timeout)

    @property
    def browser(self):
        return self._browser
