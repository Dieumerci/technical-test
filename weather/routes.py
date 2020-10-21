from flask import request, url_for, flash, redirect, session,jsonify
from flask import render_template
from flask_security import current_user, login_required,url_for_security
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
import requests
import os

from weather.models import *
from weather.models.weather import WeatherModel


def get_weather_data(data):
    SECRET_KEY = os.environ.get("API_KEY")
    API_URL = f'http://api.openweathermap.org/data/2.5/weather?q={data}&appid={SECRET_KEY}'
    req = requests.get(API_URL.format(API_URL.name)).json()
    return req

@app.route('/')
def home():
    weather_data_cities = WeatherModel.query.all()
    weather_data = []

    for weather_data_city in weather_data_cities:
        req = get_weather_data(weather_data_city.name)
        weather_dict = {
            'city': weather_data_city.name,
            'description': req['weather'][0]['description'],
            'temperature': req['main']['temp'],
            'temperature_min': req['main']['temp_min'],
            'temperature_max': req['main']['temp_max'],
            'humidity': req['main']['humidity'],
            'country_code': req['sys']['country'],
            'icon':req['weather'][0]['icon']
        }

        weather_data.append(weather_dict)
    return render_template('layout.html', weather_data=weather_data)

@app.route('/', methods=['POST'])
def home_post():
    data_error = ''
    data = request.form.get('city')
    if data:
        data_exists = WeatherModel.query.filter_by(name= data).first()

        if not data_exists:
            new_weather_data = get_weather_data(data)

            if new_weather_data['cod'] == 200:
                new_data_obj = WeatherModel(name=data)
                db.session.add(new_data_obj)
                db.session.commit()
            else:
                data_error = 'Data could not be found in API'
        else:
            data_error = 'Data already exists in the data base'

    return redirect(url_for('home'))