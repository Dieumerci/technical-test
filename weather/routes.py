from flask import request, url_for, flash, redirect, session,jsonify
from flask import render_template
from flask_security import current_user, login_required,url_for_security
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
import requests
import os

from weather.models import *

@app.route('/')
def home():
    API_URL = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=c6efa00662ece7b2952527c32ced8914'
    city = 'Johannesburg'
    req = requests.get(API_URL.format(city)).json()

    weather_dict = {
        'city': city,
        'description': req['weather'][0]['description'],
        'temperature': req['main']['temp'],
        'temperature_min': req['main']['temp_min'],
        'temperature_max': req['main']['temp_max'],
        'humidity': req['main']['humidity'],
        'country_code': req['sys']['country'],
        'icon':req['weather'][0]['icon']
    }


    return render_template('layout.html', weather_dict=weather_dict)