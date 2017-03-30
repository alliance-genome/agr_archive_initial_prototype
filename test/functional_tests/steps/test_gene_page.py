from behave import *


@when('we open the "{id}" gene page')
def step_impl(context, id):
    context.browser.visit("/gene/" + id)


@then('the gene page will return')
def step_impl(context):
    assert context.failed is False


@then('it will show the gene symbol as "{symbol}"')
def step_impl(context, symbol):
    assert symbol in context.browser.find_by_id('symbol-value').text

