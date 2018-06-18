from behave import given, when, then

from page import relying_party, idp


NAMESPACE = 'citizen-name'


@given(u'Ensure user `{user}` is in system')
def ensure_user(context, user):
    home_page = idp.UserHomePage(NAMESPACE, user)
    if not home_page.is_valid():
        create_page = idp.CreateIdentityPage()
        create_page.create_identity(NAMESPACE, user)
        create_page.assert_create_success()


@when(u'{user} request to verify identity')
def create_request(context, user):
    request_page = relying_party.CreateRequestPage()
    
    result_page = request_page.create_request(NAMESPACE, user, 300)
    context.result_page = result_page
    context.request_id = result_page.request_id
    

@when(u'{user} successfully authenticate with IdP')
def authenticate(context, user):
    pass


@when(u'{user} approve the request')
def approve_request(context, user):
    idp_home_page = idp.UserHomePage(NAMESPACE, user)
    idp_home_page.approve_request(context.request_id)

@then(u'The request become fullfiled')
def assert_request_status(context): 
    context.result_page.assert_status_verified()
