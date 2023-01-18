from django.core.exceptions import ValidationError

import requests
import logging
import re
from .models import EnquiryType, TemperatureUnit

logger = logging.getLogger(__name__)

WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"
# To obtain a key, you just need to create an account on their site. It is free
APP_ID = "90aa2e437263cd338605e7ec7f73c38f"


def get_weather(enquiry_type, city_param, country_code="", temperature_unit=TemperatureUnit.CELSIUS):
    result = None
    params = {}

    if enquiry_type is None or city_param is None:
        logger.error("Invalid argument: enquiry type and city param")
        return result

    args = [city_param, country_code]
    if enquiry_type == EnquiryType.BY_CITY_NAME:
        params['q'] = ','.join(filter(None, args))
    elif enquiry_type == EnquiryType.BY_ZIP_CODE:
        params['zip'] = ','.join(filter(None, args))
    else:
        logger.error("Unknown enquiry type %s", enquiry_type)
        return result

    # by default the value of units is considered Kelvin in the OpenWeatherMap API
    if temperature_unit == TemperatureUnit.CELSIUS:
        params['units'] = 'metric'
    elif temperature_unit == TemperatureUnit.FAHRENHEIT:
        params['units'] = 'imperial'

    params['appid'] = APP_ID
    response = requests.get(WEATHER_API_URL, params)
    logger.debug("Request: %s, Response: %s, Status code: %s",
                 response.request, response.content, response.status_code)
    if response.ok:
        try:
            result = response.json()
        except ValueError as e:
            logger.error("Exception raised in decoding json response[%s]: %s", response, str(e))

    return result


def get_element(dictionary, key_1, key_2):
    nested_dict = dictionary.get(key_1)
    if nested_dict is not None and isinstance(nested_dict, dict):
        return nested_dict.get(key_2)


def get_orientation(degree):

    if degree is not int and (degree < 0 or degree > 360):
        return None

    degree_coming_direction = {
        0: 'North',
        45: 'North East',
        90: 'East',
        135: 'South East',
        180: 'South',
        225: 'South West',
        270: 'West',
        315: 'North West'
    }

    min_diff = 360
    result = degree_coming_direction[0]
    for d in degree_coming_direction.keys():
        diff = abs(degree - d)
        if diff < min_diff:
            min_diff = diff
            result = degree_coming_direction[d]
    return result


def validate_string(value):
    p = re.compile('[a-zA-Z\-\_]+', re.IGNORECASE)
    if not p.match(value):
        raise ValidationError(
            ('%(value) is not string'),
            params={'value': value},
        )


def validate_number(value):
    p = re.compile('[0-9]+')
    if not p.match(value):
        raise ValidationError(
            ('%(value) is not number'),
            params={'value': value},
        )