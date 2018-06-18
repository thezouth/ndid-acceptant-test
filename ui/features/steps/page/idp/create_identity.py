from typing import Optional
import logging

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as expect
from hamcrest import assert_that, contains_string

from ..base import PageObject
from .common import BASE_PATH


class CreateIdentityPage(PageObject):
    def __init__(self, browser: Optional[WebDriver] = None):
        super().__init__(browser)
        self._browser.get(f'{BASE_PATH}/identity')

    def create_identity(self, namespace: str, identifier: str):
        self.fill_namespace(namespace)
        self.fill_identifier(identifier)
        self.submit()

    def assert_create_success(self):
        alert_box = self._wait().until(expect.alert_is_present())
        assert_that(alert_box.text, contains_string('Identity created'))

    def fill_namespace(self, namespace: str):
        self._browser.find_element_by_id('namespace')\
            .send_keys(namespace)
    
    def fill_identifier(self, identifier: str):
        self._browser.find_element_by_id('identifier')\
            .send_keys(identifier)
    
    def submit(self):
        self._browser.find_element_by_id('createNewIdentity')\
            .click()
