#-----------------------------------------------------------------------------
# Name:        XandaWebHost.py
#
# Purpose:     Flask route test program. 
# Author:      Yuancheng Liu
#
# Created:     2019/09/11
# Copyright:   YC @ Singtel Cyber Security Research & Development Laboratory
# License:     YC
#-----------------------------------------------------------------------------

# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ii-templates
import io, sys
import json
import random
import time
import serial
import glob
import platform
from struct import unpack
from datetime import datetime
from functools import partial
# import flask module to create the server.
from flask import Flask, render_template, flash, redirect, Response
from flask_wtf import FlaskForm # pip install flask-wtf
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

import ConfigLoader as loader
import XandaGlobal as gv
import XAKAsensorComm as xcomm
from XandaGlobal import Config


application = Flask(__name__, static_url_path='/static')
application.config.from_object(Config)

#-----------------------------------------------------------------------------
@application.route('/')
@application.route('/index')
def index():
    user = {
        'username': ' Welcome to access the XAKA[Xandar Kardian] people counting sensor '}
    posts = [
        {
            'author': {'username': 'New IOT user'},
            'body': 'The user has not logged in yet.'
        },
    ]
    return render_template('index.html', title='Sign in', user=user, posts=posts)

#-----------------------------------------------------------------------------
@application.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        userDict = gv.iUserMgr.getJson()
        if str(form.username.data) in userDict.keys():
            if str(userDict[form.username.data]) == str(form.password.data) :
                flash('Login requested for user {}, remember_me={}'.format(
                    form.username.data, form.remember_me.data))
                return redirect('/chart')
        else:
            flash('User or password incorrect, please login again')
            return redirect('/index')

    return render_template('login.html', title='Sign In', form=form)

#-----------------------------------------------------------------------------
@application.route('/chart')
def chart():
    return render_template('chart.html')

@application.route('/chart-data') # the route component must match the related <dev> in the html file.
def chart_data():
    def generate_sensor_data():
        while True:
            dataList = gv.iCommReader.fetchSensorData()
            peopleNum = int(dataList[27])
            json_data = json.dumps(
                #{'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': gv.iCommReader.readComm() })
                {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': peopleNum })
            #print(f"data:{json_data}\n\n")
            yield "data:"+json_data+"\n\n"
            time.sleep(1)
    return Response(generate_sensor_data(), mimetype='text/event-stream')

#-----------------------------------------------------------------------------
class LoginForm(FlaskForm):
    """ Form to handle the user login."""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
if __name__ == '__main__':
    gv.iUserMgr = loader.ConfigLoader(gv.USER_PWD, mode='r', filterChars=('#', '', '\n'))
    gv.iCommReader = xcomm.XAKAsensorComm(gv.DE_COMM, simuMd=gv.gSimulationMode)
    gv.iCommReader.setSerialComm(searchFlag=True)
    print('Start the web server.')
    application.run(debug=False, threaded=True)
    # application.run(host= "0.0.0.0", debug=False, threaded=True) # use 0.0.0.0 if we want access the web from other computer.
    print('Finished')
