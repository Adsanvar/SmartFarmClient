from flask import Flask, render_template, request, flash, Blueprint, session, redirect, url_for, send_file, Response
import requests
from flask_apscheduler import APScheduler
import datetime
import RPi.GPIO as GPIO
from time import sleep
from . import create_app
import os
# import picamera
# import cv2
# import io
# import socket

home = Blueprint('home', __name__)
scheduler = APScheduler()
scheduler.start()
every=4
# light_hours = 24
# every_fan_hours = 22
every_day = 24
duration = 12
# airstone_duration = 120
# light_duration = 64800 #ON
light_duration_off = 14400 #OFF
# fan_duration_off = 14400 #OFF 4 hours
fan_duration_off = 43200 #OFF 12 hours
app = create_app()
# vc = cv2.VideoCapture(0) 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW) # EXHAUST FAN
GPIO.setup(16, GPIO.OUT, initial=GPIO.LOW)  # LIGHTS
# GPIO.setup(11, GPIO.OUT, initial=GPIO.HIGH) # FAN
GPIO.setup(13, GPIO.OUT, initial=GPIO.HIGH) # MISTER

#fan = LED(17, initial_value=True) #Set's it High (since our Relays are triggered on a low architecture)
#mister = LED(27, initial_value=True)

#This Route is the index page (landing page)
@home.route('/', methods=['GET'])
def index():
    return render_template('index.html')
   
@home.route('/', methods=['POST'])
def clicked():
    if 'data' in request.form:
        r = requests.get("https://agriculta.loca.lt/getSomeData")
        print(r.headers)
        print(r.status_code)
        print(r.content)
        flash('Data Retrieved', 'success')
        return render_template('index.html')
    # elif 'login' in request.form:
    #     usr = request.form.get('username')
    #     pas = request.form.get('password')
    #     if usr == 'admin' and pas == 'admin':
    #         return render_template('stream.html')
    #     else:
    #         flash('Invalid Credentials', 'error')
    #         return render_template('index.html')
    else:
        flash('Password Successfully Changed', 'success')
        return render_template('index.html')

@home.route('/getSomeData', methods=['GET'])
def getSomeData():
    return "HELLO THIS IS A STRING BEING RETURN BECAUSE YOU CALLED THIS ROUTE"

@home.route('/gitPull', methods=['GET'])
def gitPull():
    try:
        # command = os.popen('./~/Documents/SmartFarmClient/gitPull.sh')
        command = os.popen('pwd')
        response = command.read()
        return response , 200
    except:
        raise
@home.route('/logs', methods=['GET'])
def logs():
    command = os.popen('ls logs')
    response = command.read()
    return response , 200

# def gen():
#     while True:
#         rval, frame = vc.read()
#         cv2.imwrite('t.jpg', frame)
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')

# @home.route('/videoFeed', methods=['GET'])
# def videoFeed():
#     return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

# @home.route('/test', methods=['GET'])
# def test():
#     os.system('lt --port 5005 --subdomain agriculta')
#     return "success"

# @home.route('/turnOnTest', methods=['GET'])
# def turnOnFan():
#     now = datetime.datetime.now()
#     # delta = now + datetime.timedelta(minutes = 1)
#     print("from link")
#     # app.logger.info("LIGHTS - START: {} ".format(now))
#     print("{} - Test Started".format(now))
#     GPIO.output(18, GPIO.HIGH)
#     print("18 - HIGH")
#     GPIO.output(16, GPIO.HIGH)
#     print("16 - HIGH")
#     GPIO.output(11, GPIO.HIGH)
#     print("11 - HIGH")
#     GPIO.output(13, GPIO.HIGH)
#     print("13 - HIGH")
#     sleep(25)
#     GPIO.output(18, GPIO.LOW)
#     print("18 - LOW")
#     GPIO.output(16, GPIO.LOW)
#     print("16 - LOW")
#     GPIO.output(11, GPIO.LOW)
#     print("11 - LOW")
#     GPIO.output(13, GPIO.LOW)
#     print("13 - LOW")
#     print("{} - Test Finished".format(now))
#     # app.logger.info("LIGHTS - ENDED: {}".format(now))
#     return "success", 200

@scheduler.task('interval', id='light', hours=every_day)
def activate_lights():
    now = datetime.datetime.now()
    # delta = now + datetime.timedelta(minutes = 1)
    app.logger.info("LIGHTS OFF - START: {} ".format(now))
    print("{} - LIGHTS TURNED OFF".format(now))
    GPIO.output(16, GPIO.HIGH)
    sleep(light_duration_off)
    # sleep(30)
    GPIO.output(16, GPIO.LOW)
    print("LIGHTS OFF Finished")
    app.logger.info("LIGHTS OFF - ENDED: {}".format(now))

@scheduler.task('interval', id='exhaust_fan', hours=every_day)
def activate_exhaust():
    print("exhuast off")
    now = datetime.datetime.now()
    # delta = now + datetime.timedelta(minutes = 1)
    app.logger.info("EXHAUST OFF - START: {} ".format(now))
    print("{} - EXHAUST TURNED OFF".format(now))
    GPIO.output(18, GPIO.HIGH)
    sleep(fan_duration_off)
    # sleep(30)
    GPIO.output(18, GPIO.LOW)
    print("EXHAUST OFF Finished")
    app.logger.info("EXHAUST OFF - ENDED: {}".format(now))

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

# @scheduler.task('interval', id='fan', minutes=every)
# def activate_fan():
#     now = datetime.datetime.now()
#     # delta = now + datetime.timedelta(minutes = 1)
#     # sleep(15)
#     app.logger.info("FAN - START: {} ".format(now))
#     print("{} - FAN Started".format(now))
    
#     GPIO.output(11, GPIO.LOW)
#     sleep(duration+5)
#     GPIO.output(11, GPIO.HIGH)

#     print("Fan Finished")
#     app.logger.info("FAN - ENDED: {}".format(now))

# @scheduler.task('interval', id='airstone', minutes=every)
# def activate_fan():
#     now = datetime.datetime.now()
#     # delta = now + datetime.timedelta(minutes = 1)
#     # sleep(15)
#     app.logger.info("Airstone - START: {} ".format(now))
#     print("{} - Airstone Started".format(now))
    
#     GPIO.output(11, GPIO.LOW)
#     sleep(airstone_duration)
#     GPIO.output(11, GPIO.HIGH)

#     print("Airstone Finished")
#     app.logger.info("FAN - ENDED: {}".format(now))

