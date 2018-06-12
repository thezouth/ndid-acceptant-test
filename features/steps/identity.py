from behave import given, when, then
from hamcrest import assert_that, contains_string
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


IDP_HOST = 'http://localhost:8000'

@given('User enters IdP')
def enter_idp(context):
    context.user_browser = webdriver.Chrome(executable_path='/Users/Admin/Documents/chromedriver')
    context.user_browser.get(IDP_HOST + '/identity')


@when('User creates identity {namespace}:{identifier}')
def create_identity(context, namespace, identifier):
    namespace_elem = context.user_browser.find_element_by_id('namespace')
    identifier_elem = context.user_browser.find_element_by_id('identifier')
    submit_btn = context.user_browser.find_element_by_id('createNewIdentity')
    
    namespace_elem.send_keys(namespace)
    identifier_elem.send_keys(identifier)
    submit_btn.click()


@then('System successfully created the new id')
def validate_identity_create_response(context):
    driver_wait = WebDriverWait(context.user_browser, 10)
    alert = driver_wait.until(expected_conditions.alert_is_present())
    assert_that(alert.text, contains_string('Identity created'))
