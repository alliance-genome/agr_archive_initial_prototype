from behave import *


@given('we open the search url querying for "{query}"')
def step_impl(context, query):
    context.browser.visit("/search?q=" + query)


@When('the search page returns')
def step_impl(context):
    assert context.failed is False


@then('"{linktext}" will be on the first page of search results')
def step_impl(context, linktext):
    assert context.browser.find_by_link_text(linktext)

