# weather-app
Weather web app backed by OpenWeatherAPI in Python/Django

## Introduction
This web app provides a nice simple interface to get the weather information of any city that you wish.
You can make an enquiry by city name or postal code (zip code) accompanied with a country name.

### How Does It Work?
This app actually consumes the OpenWeatherMap RESTful API (http://api.openweathermap.org/data/2.5/weather).
To do so, it gathers the place information from you, make a rest call to the above api, parse, and eventually
display the returned api response for you.

### To Run
First, you need to create an account on the weather provide website (http://api.openweathermap.org/).
Then, get your key and copy it in service.py at line 12:
    APP_ID = "replace-with-your-key"
Finally, execute the following commands:
$ cd <path-to-the-project-dir>
$ python manage.py runserver

In your browser: http://localhost:8000/weather/

To get more information on how to run django web apps, please check out: https://docs.djangoproject.com/en/2.0/

### Main Technologies Used
Python 3, Django 2, and Rest
