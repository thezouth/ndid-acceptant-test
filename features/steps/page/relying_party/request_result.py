from hamcrest.core.core.isnone import not_none
from hamcrest import assert_that
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.common.by import By

from ..base import PageObject

class RequestResultPage(PageObject):
    def __init__(self, browser: WebDriver):
        super().__init__(browser)
        self._request_id = self._get_request_id()
    
    @property
    def request_id(self):
        return self._request_id

    def assert_status_verified(self):
        status_locator = (By.ID, 'status')
        verified_mssage = 'Verification Successful!'

        self._wait().until(
            expect.text_to_be_present_in_element(status_locator, verified_mssage))

    def _get_request_id(self) -> str:
        request_id_elem = self._wait().until(
            expect.visibility_of_element_located((By.ID, 'requestId')))
        
        assert_that(request_id_elem, not_none())
        return request_id_elem.text.split()[-1]

