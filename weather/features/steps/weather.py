from behave import *
from selenium.webdriver.support.select import Select


@given('I choose "{enquiry_type}" for type, enter "{enquiry_param}", and choose "{country_code}" for country and  "{temperature_unit}" for unit')
def step_impl(context, enquiry_type, enquiry_param, country_code, temperature_unit):
    browser = context.browser
    browser.get('http://localhost:8000/weather/')

    if enquiry_type == 'City':
        browser.find_element_by_id('enquiry_type1').click()
    elif enquiry_type == 'Zip Code':
        browser.find_element_by_id('enquiry_type2').click()

    browser.find_element_by_id('enquiry_param').send_keys(enquiry_param)
    select = Select(browser.find_element_by_id('country_code'))
    select.select_by_value(country_code)

    if temperature_unit == 'Celsius':
        browser.find_element_by_id('temperature_unit1').click()
    elif temperature_unit == 'Fahrenheit':
        browser.find_element_by_id('temperature_unit2').click()

    browser.find_element_by_id('ok').click()


@then('I should see the weather info for "{text}" in "{temperature_unit}"')
def step_impl(context, text, temperature_unit):
    browser = context.browser

    assert browser.current_url == "http://localhost:8000/weather/result/"

    result = browser.find_element_by_tag_name("body").text.lower()
    assert "error" not in result
    assert text.lower() in result

    if temperature_unit == 'Celsius':
        assert "°c" in result
    elif temperature_unit == 'Fahrenheit':
        assert "°f" in result


@then('I should see the error page for "{text}" in "{temperature_unit}"')
def step_impl(context, text, temperature_unit):
    browser = context.browser

    assert browser.current_url == "http://localhost:8000/weather/result/"

    result = browser.find_element_by_tag_name("body").text.lower()
    assert "error" in result
    assert text.lower() in result
    assert temperature_unit.lower() in result
