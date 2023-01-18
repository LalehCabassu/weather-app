from django.test import TestCase

from weather import services, models

CITY_NAME = "Salt Lake City"
COUNTRY_CODE = "us"
ZIP_CODE = "84102"


class ServiceTests(TestCase):

    def test_get_weather_by_city_name(self):
        result = services.get_weather(services.EnquiryType.BY_CITY_NAME, CITY_NAME)

        # verify the response contents
        self.assertIsNotNone(result)
        self.assertIsNotNone(result.get('coord'))
        self.assertIsNotNone(result.get('weather'))
        self.assertIsNotNone(result.get('main'))
        self.assertIsNotNone(result.get('sys'))
        self.assertEqual(CITY_NAME, result.get('name'))

    def test_get_weather_by_city_name_country_code(self):
        result = services.get_weather(services.EnquiryType.BY_CITY_NAME, CITY_NAME, COUNTRY_CODE)

        # verify the response contents
        self.assertIsNotNone(result)
        self.assertIsNotNone(result.get('coord'))
        self.assertIsNotNone(result.get('weather'))
        self.assertIsNotNone(result.get('main'))
        self.assertIsNotNone(result.get('sys'))
        self.assertEqual(CITY_NAME, result.get('name'))

    def test_get_weather_by_zip_code(self):
        result = services.get_weather(services.EnquiryType.BY_ZIP_CODE, ZIP_CODE)

        # verify the response contents
        self.assertIsNotNone(result)
        self.assertIsNotNone(result.get('coord'))
        self.assertIsNotNone(result.get('weather'))
        self.assertIsNotNone(result.get('main'))
        self.assertIsNotNone(result.get('sys'))
        self.assertEqual(CITY_NAME, result.get('name'))

    def test_get_weather_by_zip_code_country_code(self):
        result = services.get_weather(services.EnquiryType.BY_ZIP_CODE, ZIP_CODE, COUNTRY_CODE)

        # verify the response contents
        self.assertIsNotNone(result)
        self.assertIsNotNone(result.get('coord'))
        self.assertIsNotNone(result.get('weather'))
        self.assertIsNotNone(result.get('main'))
        self.assertIsNotNone(result.get('sys'))
        self.assertEqual(CITY_NAME, result.get('name'))

    def test_get_weather_by_none_arguments(self):
        result = services.get_weather(None, None)
        self.assertIsNone(result)

    def test_get_weather_by_invalid_enquiry_type(self):
        result = services.get_weather(4, "nowhere")
        self.assertIsNone(result)

    def test_validate_string(self):
        services.validate_string(CITY_NAME)
        services.validate_string(models.EnquiryType.BY_CITY_NAME.name)
        services.validate_string("Salon-de-provence")

    def test_validate_number(self):
        services.validate_number(ZIP_CODE)

    def test_get_element(self):
        result = services.get_element({'weather': {'main': 'Sunny'}}, 'weather', 'main')
        self.assertEqual('Sunny', result)

    def test_get_element_fail(self):
        result = services.get_element({'weather': 'main'}, 'weather', 'main')
        self.assertIsNone(result)

    def test_get_orientation(self):
        result = services.get_orientation(100)
        self.assertIsNotNone(result)
        self.assertEqual('East', result)

    def test_get_orientation_invalid_degree(self):
        result = services.get_orientation(400)
        self.assertIsNone(result)