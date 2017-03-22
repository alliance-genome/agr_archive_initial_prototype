from behave import *


@when('we open the gene page')
def step_impl(context):
    context.browser.visit("/gene/ZDB-GENE-990415-72")


@then('the gene page will return')
def step_impl(context):
    assert context.failed is False


@then('it will show the gene symbol')
def step_impl(context):
    assert "fgf8a" in context.browser.find_by_id('symbol-value').text

