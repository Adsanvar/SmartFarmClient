from flask import Flask, render_template, request, flash, Blueprint, session, redirect, url_for
import requests
from flask_apscheduler import APScheduler
import datetime
import RPi.GPIO as GPIO
from time import sleep
from . import create_app

home = Blueprint('home', __name__)
scheduler = APScheduler()
scheduler.start()
every=20
duration = 180
app = create_app()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(13, GPIO.OUT, initial=GPIO.HIGH)

#fan = LED(17, initial_value=True) #Set's it High (since our Relays are triggered on a low architecture)
#mister = LED(27, initial_value=True)
#This Route is the index page (landing page) -Adrian
@home.route('/', methods=['GET'])
def index():
    return render_template('index.html')
   
@home.route('/', methods=['POST'])
def clicked():
    if 'data' in request.form:
        r = requests.get("https://witty-hound-43.loca.lt/getSomeData")
        print(r.headers)
        print(r.status_code)
        print(r.content)
        flash('Data Retrieved', 'success')
        return render_template('index.html')

    else:
        flash('Password Successfully Changed', 'success')
        return render_template('index.html')

@home.route('/getSomeData', methods=['GET'])
def getSomeData():
    return "HELLO THIS IS A STRING BEING RETURN BECAUSE YOU CALLED THIS ROUTE"

@scheduler.task('interval', id='mist', minutes=every)
def activate_mister():
    now = datetime.datetime.now()
    # delta = now + datetime.timedelta(minutes = 1)
    app.logger.info("MISTING - START: {} ".format(now))
    print("{} - Mister Started".format(now))
    GPIO.output(13, GPIO.LOW)
    sleep(duration)
    GPIO.output(13, GPIO.HIGH)
    print("mister Finished")
    app.logger.info("MISTING - ENDED: {}".format(now))

@scheduler.task('interval', id='fan', minutes=every)
def activate_fan():
    now = datetime.datetime.now()
    # delta = now + datetime.timedelta(minutes = 1)
    sleep(30)
    app.logger.info("FAN - START: {} ".format(now))
    print("{} - Fan Started".format(now))
    
    GPIO.output(11, GPIO.LOW)
    sleep(15)
    GPIO.output(11, GPIO.HIGH)
    sleep(30)
    GPIO.output(11, GPIO.LOW)
    sleep(15)
    GPIO.output(11, GPIO.HIGH)
    sleep(30)
    GPIO.output(11, GPIO.LOW)
    sleep(15)
    GPIO.output(11, GPIO.HIGH)
    sleep(30)
    GPIO.output(11, GPIO.LOW)
    sleep(15)
    GPIO.output(11, GPIO.HIGH)
    print("Fan Finished")
    app.logger.info("FAN - ENDED: {}".format(now))
