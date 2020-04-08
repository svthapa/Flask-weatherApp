from flask import render_template, url_for, request, redirect, flash, jsonify, Blueprint
import json
import requests
import os.path
from flask_sqlalchemy import SQLAlchemy

bp = Blueprint('weatherApp', __name__)

db= SQLAlchemy()
class City(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50), nullable=False)

def get_weather_data(city):
    url= f'http://api.openweathermap.org/data/2.5/weather?q={ city }&units=imperial&appid=2a75707d5ff8ff84e20e88628c9d7ecf'
    r = requests.get(url).json()#request
    return r

@bp.route('/')
def home_get():

    cities=City.query.all()
    weather_data=[]

    for city in cities:
        r= get_weather_data(city.name)
        context={
            'city': city.name,
            'temp': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }

        weather_data.append(context)
    return render_template('weather.html', weather_data=weather_data)

@bp.route('/', methods=['POST'])
def home_post():
    if request.method == "POST":
        new_city = request.form['city']
        existing_city = City.query.filter_by(name=new_city).first()
        if not existing_city:
            new_city_data = get_weather_data(new_city)
            if new_city_data['cod'] == 200:
                city_obj = City(name=new_city)
                db.session.add(city_obj)
                db.session.commit()
                flash('City Added.', category='success')
            else:
                flash('City Does Not Exist. Try Again.', category='danger')

        else:
            flash('City Already Added.', category='danger')
            return redirect(url_for('weatherApp.home_get'))

    return redirect(url_for('weatherApp.home_get'))

@bp.route('/delete/<city>')
def delete_city(city):
    del_city= City.query.filter_by(name=city).first()
    db.session.delete(del_city)
    db.session.commit()
    flash('City Has Been Deleted.', 'success')

    return redirect(url_for('weatherApp.home_get'))
