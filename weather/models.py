from enum import Enum


class EnquiryType(Enum):
    BY_CITY_NAME = 1
    BY_ZIP_CODE = 2


class TemperatureUnit(Enum):
    CELSIUS = 1
    FAHRENHEIT = 2


class Message(object):
    def __init__(self, type, message, default=False):
        self.type = type
        self.message = message
        self.default = default

    def checked(self):
        return "checked" if self.default else ""
