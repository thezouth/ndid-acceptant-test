from typing import Optional

from selenium.webdriver.remote.webdriver import WebDriver

from ..base import PageObject
from .common import BASE_PATH
from .request_result import RequestResultPage

class CreateRequestPage(PageObject):
    def __init__(self, browser: Optional[WebDriver] = None):
        super().__init__(browser)
        self._browser.get(f'{BASE_PATH}')

    def create_request(self, namespace: str, identifier: str,
                       timeout: int = 300) -> RequestResultPage:
        self.fill_namespace(namespace)
        self.fill_identifier(identifier)
        self.fill_timeout(timeout)
        self.submit()

        return RequestResultPage(self._browser)

    def fill_namespace(self, namespace: str):
        self._browser.find_element_by_id('namespace')\
            .send_keys(namespace)

    def fill_identifier(self, identifier: str):
        self._browser.find_element_by_id('identifier')\
            .send_keys(identifier)
    
    def fill_timeout(self, timeout: int):
        self._browser.find_element_by_id('timeout')\
            .send_keys(str(timeout))
    
    def submit(self):
        self._browser.find_element_by_id('verify')\
            .click()
