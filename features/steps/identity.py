from time import time

from behave import given, when, then

from page import idp

@given('User enters IdP')
def enter_idp(context):
    context.create_page = idp.CreateIdentityPage()


@when('User creates a new identity')
def create_identity(context):
    namespace = 'test'
    identifier = str(time())
    context.create_page.create_identity(namespace, identifier)


@then('System successfully created the new id')
def validate_identity_create_response(context):
    context.create_page.assert_create_success()

