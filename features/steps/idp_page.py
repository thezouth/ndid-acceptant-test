import logging

from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException

IDP_HOST = 'http://localhost:8000'
TIMEOUT = 3

class IdpPage():
    def __init__(self, context, namespace, identifier):
        self.context = context
        self.namespace = namespace
        self.identifier = identifier
        self.browser = webdriver.Chrome(executable_path='/Users/Admin/Documents/chromedriver')
        self.driver_wait = webdriver.support.ui.WebDriverWait(self.browser, TIMEOUT)


    def open(self, url):    
        self.page = url    
        self.browser.get(IDP_HOST + url)


    def goto_identity(self):
        self.open(f'/identity')
        self.page = 'identity'
        self.form = {}
        self.form['namespace'] = self.browser.find_element_by_id('namespace')
        self.form['identifier'] = self.browser.find_element_by_id('identifier')
        self.form['submit_btn'] = self.browser.find_element_by_id('createNewIdentity')


    def goto_home(self):
        self.open(f'/home/{self.namespace}/{self.identifier}')

    
    def wait_for_data(self):
        self.driver_wait.until_not(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '.loading-indicator')))


    def approve(self, request_id):
        req_elem = self.driver_wait.until(find_request_element(request_id))
        req_elem.find_element_by_css_selector('.btn-success').click()
    


class find_request_element():
    def __init__(self, request_id):
        self.request_id = request_id
    
    def __call__(self, driver):
        logging.debug('Request: %s', self.request_id)
        items = driver.find_elements_by_css_selector('.request-list-item')
        try:
            for item in items:
                request_id_elem = item.find_element_by_css_selector('.request-info > div')
                logging.debug(request_id_elem.text)
                if self.request_id in request_id_elem.text:
                    return item
        except StaleElementReferenceException as ser:
            logging.debug('Handle StaleElementReferenceException')
            return False

        return False