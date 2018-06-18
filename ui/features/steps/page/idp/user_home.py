from typing import Optional
import logging

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions  as expect
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (UnexpectedAlertPresentException, 
    TimeoutException, StaleElementReferenceException)

from ..base import PageObject
from .common import BASE_PATH


class UserHomePage(PageObject):
    def __init__(self, namespace: str, identifier: str, 
                 browser: Optional[WebDriver] = None):
        super().__init__(browser)
        self._browser.get(f'{BASE_PATH}/home/{namespace}/{identifier}')

    def is_valid(self) -> bool:
        try:
            loading_present = expect.visibility_of_element_located((By.CSS_SELECTOR, '.loading-indicator'))
            self._wait().until_not(loading_present)
            return True
        except (UnexpectedAlertPresentException, TimeoutError):
            return False
    
    def approve_request(self, request_id: str):
        request_elem = self._wait().until(self._find_request_element(request_id))

        approve_button = request_elem.find_element_by_css_selector('.btn-success')
        approve_button.click()

    def _find_request_element(self, request_id):
        def __func(driver):
            logging.debug('Request: %s', request_id)
            items = driver.find_elements_by_css_selector('.request-list-item')
            try:
                for item in items:
                    request_id_elem = item.find_element_by_css_selector('.request-info > div')
                    logging.debug(request_id_elem.text)
                    if request_id in request_id_elem.text:
                        return item

            except StaleElementReferenceException:
                logging.debug('Handle StaleElementReferenceException')
                return False

            return False

        return __func