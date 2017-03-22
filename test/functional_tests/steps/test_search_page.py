from behave import *


@given('we open the search url querying for "{query}"')
def step_impl(context, query):
    context.browser.visit("/search?q=" + query)


@When('the search page returns')
def step_impl(context):
    assert context.failed is False


@then('"{id}" will be part of the first page of search results')
def step_impl(context, id):
    assert context.browser.find_by_link_text(id)

