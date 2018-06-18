from behave import when, then

import requests
import logging
from time import time

from hamcrest import assert_that, equal_to
import id_provider


@when('User create a new identity')
def create_new_identity(context):
    namespace = 'test'
    identifier = str(time())
    
    context.response = id_provider.create_identity(namespace, identifier, 2.3)


@then('Id Provider successfully created the new identity')
def assert_create_result(context):
    resp = context.response
    assert_that(resp.status_code, equal_to(200))
    logging.info(resp.json())


@then('Underlying block contains identity created block')
def assert_block_exist(context):
    pass
