from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from datetime import *

from .models import *
from .services import *

logger = logging.getLogger(__name__)


@require_http_methods(["GET"])
def index(request):
    context = {'message': "Let's check out the weather!",
               'enquiry_types': [
                   Message(EnquiryType.BY_CITY_NAME.name, "City", True),
                   Message(EnquiryType.BY_ZIP_CODE.name, "Zip Code")],
               'temperature_units': [
                   Message(TemperatureUnit.CELSIUS.name, "Celsius", True),
                   Message(TemperatureUnit.FAHRENHEIT.name, "Fahrenheit")]
               }
    logger.debug("Rendering index: %s", context)
    return render(request, 'weather/index.html', context)


@require_http_methods(["POST"])
def result(request):
    enquiry_type = request.POST['enquiry_type']
    enquiry_param = request.POST['enquiry_param']
    country_code = request.POST['country_code']
    temperature_unit = request.POST['temperature_unit']

    try:
        validate_string(enquiry_type)
        enquiry_type_enum = EnquiryType[enquiry_type]
        if enquiry_type_enum == EnquiryType.BY_CITY_NAME:
            validate_string(enquiry_param)
        else:
            validate_number(enquiry_param)
        validate_string(temperature_unit)
        temperature_unit_enum = TemperatureUnit[temperature_unit]
    except ValidationError:
        logger.error("Exception raised in validating enquiry params %s, %s, %s, %s",
                     enquiry_type, enquiry_param, country_code, temperature_unit)
        context = {
            'message': 'Error in validating enquiry params: ' +
                       ', '.join(filter(None, [enquiry_type, enquiry_param, country_code, temperature_unit]))
        }
        return render(request, 'weather/error.html', context)
    else:
        logger.debug("Calling Weather API with params: %s, %s, %s, %s", enquiry_type, enquiry_param, country_code, temperature_unit)
        response_weather = get_weather(enquiry_type_enum, enquiry_param, country_code, temperature_unit_enum)
        logger.debug("Raw response of Weather API: %s", response_weather)

        if response_weather is not None:
            try:
                context = {
                    'city': response_weather.get('name'),
                    'country': get_element(response_weather, 'sys', 'country'),
                    'temperature': get_element(response_weather, 'main', 'temp'),
                    'temperature_min': get_element(response_weather, 'main', 'temp_min'),
                    'temperature_max': get_element(response_weather, 'main', 'temp_max'),
                    'unit': temperature_unit[0],
                    'description': response_weather.get('weather')[0].get('main'),
                    'sunrise': datetime.fromtimestamp(get_element(response_weather, 'sys', 'sunrise')).time(),
                    'sunset': datetime.fromtimestamp(get_element(response_weather, 'sys', 'sunset')).time(),
                    'humidity': get_element(response_weather, 'main', 'humidity'),
                }
            except IndexError:
                logger.error("Exception raised in parsing the weather API response")
                context = {
                    'message': 'Error in parsing the response' + response_weather +
                               'for the enquiry: ' +
                               ', '.join(filter(None, [enquiry_type, enquiry_param, country_code, temperature_unit]))
                }
                return render(request, 'weather/error.html', context)
            else:
                wind_speed = get_element(response_weather, 'wind', 'speed')
                if wind_speed is not None:
                    context['wind_speed'] = wind_speed

                wind_deg = get_element(response_weather, 'wind', 'deg')
                if wind_deg is not None:
                    try:
                        wind_deg_int = int(wind_deg)
                    except ValueError:
                        logger.error("An exception raised while parsing the wind degree")
                    else:
                        context['wind_orientation'] = get_orientation(wind_deg_int)

                clouds_all = get_element(response_weather, 'clouds', 'all')
                if clouds_all is not None:
                    context['cloud_percent'] = clouds_all

                rain_amount = get_element(response_weather, 'rain', '3h')
                if rain_amount is not None:
                    context['rain_amount'] = rain_amount

                snow_amount = get_element(response_weather, 'snow', '3h')
                if snow_amount is not None:
                    context['snow_amount'] = snow_amount

                return render(request, 'weather/result.html', context)
        else:
            context = {
                'message': 'No response for the enquiry: ' +
                           ', '. join(filter(None, [enquiry_type, enquiry_param, country_code, temperature_unit]))
            }
            return render(request, 'weather/error.html', context)