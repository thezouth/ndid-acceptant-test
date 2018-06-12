from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

from hamcrest.core.core.isnone import none, not_none
from hamcrest import assert_that, contains_string


RP_HOST = 'http://localhost:8001'
TIMEOUT = 3

class RpPage():
    def __init__(self, context, namespace, identifier):
        self.context = context
        self.namespace = namespace
        self.identifier = identifier
        self.browser = webdriver.Chrome(executable_path='/Users/Admin/Documents/chromedriver')
        self.driver_wait = webdriver.support.ui.WebDriverWait(self.browser, TIMEOUT)


    def open(self, url):
        self.page = url
        self.browser.get(RP_HOST + url)


    def goto_identity_verification(self):
        self.open('')
        self.form = {}
        self.page = 'identity_verification'
        self.form['namespace'] = self.browser.find_element_by_id('namespace')
        self.form['identifier'] = self.browser.find_element_by_id('identifier')
        self.form['timeout'] = self.browser.find_element_by_id('timeout')
        self.form['verify_btn'] = self.browser.find_element_by_id('verify')        


    def get_request_id(self):
        if self.page != 'identity_verification':
            raise Exception('you are in wrong page.')
        
        request_id_elem = self.driver_wait.until(expected_conditions.visibility_of_element_located((By.ID, 'requestId')))
        assert_that(request_id_elem, not_none())

        return request_id_elem.text.split()[-1]


    def assert_status(self, status):
        self.driver_wait.until(expected_conditions.text_to_be_present_in_element((By.CSS_SELECTOR, '#status'), status))
        assert_that(self.browser.find_element_by_id('status').text, contains_string(status))
