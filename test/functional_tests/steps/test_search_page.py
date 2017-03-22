from behave import *


@when('we open the search url for a simple search')
def step_impl(context):
    context.browser.visit("/search?q=fgf8")


@then('the search page will return')
def step_impl(context):
    assert context.failed is False


@then('it will contain the id of the search result we expect to find')
def step_impl(context):
    id_list = (o.text for o in context.browser.find_all_by_class('symbol-value'))
    assert "ZDB-GENE-990415-72" in id_list

