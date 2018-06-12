from behave import given, when, then

from idp_page import IdpPage
from rp_page import RpPage

DEFAULT_NAMESPACE = 'citizen-name'


@given(u'Ensure user `{user}` is in system')
def step_impl(context, user):    
    context.idp = IdpPage(context, DEFAULT_NAMESPACE, 'Roofimon')
    idp = context.idp
    idp.goto_home()
    idp.wait_for_data()    


@when(u'Roofimon request to verify identity')
def step_impl(context):
    context.rp = RpPage(context, DEFAULT_NAMESPACE, 'Roofimon')
    rp = context.rp
    rp.goto_identity_verification()
    rp.form['namespace'].send_keys(rp.namespace)
    rp.form['identifier'].send_keys(rp.identifier)
    rp.form['timeout'].send_keys('300')
    rp.form['verify_btn'].click()

    context.request_id = rp.get_request_id()
    

@when(u'Roofimon successfully authenticate with IdP')
def step_impl(context):
    pass


@when(u'Roofimon approve the request')
def step_impl(context):
    idp = context.idp
    idp.goto_home()
    idp.approve(context.request_id)


@then(u'The request become fullfiled')
def step_impl(context): 
    context.rp.assert_status('Verification Successful!')


