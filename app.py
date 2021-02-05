from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from datetime import datetime
from flask_caching import Cache
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError, DataRequired
import requests


app = Flask(__name__)

app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'united' 
app.config['SECRET_KEY']='LongAndRandomSecretKey'
bootstrap = Bootstrap(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

class LoginForm(FlaskForm):
    username = StringField(label=('Unesite ime:'), validators=[DataRequired()])
    submit = SubmitField(label=('Submit'))
    surname = StringField(label=('Unesite prezime:'), validators=[DataRequired()])

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/proizvodi')
def proizvodi():
    return render_template('proizvodi.html')

@app.route('/cjenik')
def cjenik():
    return render_template('cjenik.html')

@app.route('/', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    username = form.username.data
    surname = form.surname.data
    if form.validate_on_submit():
           return render_template('index.html', username = username, surname = surname)
    return render_template('login.html', form=form)

@app.route('/tečaj')
@cache.cached(timeout=60)
def tečaj():
    now = datetime.now()
    url = 'http://api.openweathermap.org/data/2.5/weather'
    parameters = {'q': 'Rovanjska', 'appid': '464b8e606097703f41f58b71f890ed3f','lang': 'hr', 'units': 'metric'}
    response = requests.get(url, parameters)
    weather = response.json()
    return render_template('tečaj.html', weather = weather, datetime = datetime, now = now)




@app.template_filter('datetime')
def fomat_datetime(value, format = '%d.%m.%Y %H:%M'):
    return datetime.fromtimestamp (value).strftime(format) 

@app.errorhandler(404)
def invalid_route(e):
    return render_template('button.html')

