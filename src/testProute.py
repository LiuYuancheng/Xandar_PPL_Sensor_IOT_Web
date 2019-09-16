#-----------------------------------------------------------------------------
# Name:        testProute.py
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
from testPGlobal import Config
from flask_wtf import FlaskForm # pip install flask-wtf
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

import testPGlobal as gv
from testPGlobal import Config

DE_COMM = 'COM3' if platform.system() == 'Windows' else '/dev/ttyUSB0'

application = Flask(__name__)
application.config.from_object(Config)

#-----------------------------------------------------------------------------
@application.route('/')
@application.route('/index')
def index():
    user = {'username' : 'test'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
    ]

    return render_template('index.html', title='Sign in', user=user, posts=posts)

#-----------------------------------------------------------------------------
@application.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if str(form.username.data) == '123' and str(form.password.data) == '123':
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

@application.route('/chart-data')
def chart_data():
    def generate_random_data():
        while True:
            json_data = json.dumps(
                {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': gv.iCommReader.readComm() })
            #print(f"data:{json_data}\n\n")
            yield "data:"+json_data+"\n\n"
            time.sleep(1)

    return Response(generate_random_data(), mimetype='text/event-stream')

#-----------------------------------------------------------------------------
class LoginForm(FlaskForm):
    """ From to handle the login.
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')



#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class SensorCom(object):
    """ Interface to store the PLC information and control the PLC through 
        by hooking to the ModBus(TCPIP).
    """
    def __init__(self, parent):
        self.serialPort = DE_COMM   # the serial port name we are going to read.
        self.serComm = None # serial comm handler used to read the sensor data. 
        self.dataList = []
        self.setSerialComm(searchFlag=True)

     #--SensorReaderFrame-----------------------------------------------------------
    def setSerialComm(self, searchFlag=False):
        """ Automatically search for the sensor and do the connection."""
        if not self.serComm is None:
            self.serComm.close()  # close the exists opened port.
            self.serComm = None 
        portList = []
        if searchFlag:
            # look for the port on different platform:
            if sys.platform.startswith('win'):
                ports = ['COM%s' % (i + 1) for i in range(256)]
            elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
                # this excludes your current terminal "/dev/tty"
                ports = glob.glob('/dev/tty[A-Za-z]*')
            elif sys.platform.startswith('darwin'):
                ports = glob.glob('/dev/tty.*')
            else:
                raise EnvironmentError('Serial Port comm connection error: Unsupported platform.')
            for port in ports:
                # Check whether the port can be open.
                try:
                    s = serial.Serial(port)
                    s.close()
                    portList.append(port)
                except (OSError, serial.SerialException):
                    pass
            print(('COM connection: the serial port can be used :%s' % str(portList)))
        # normally the first comm prot is resoved by the system.
        if not self.serialPort in portList: self.serialPort = portList[-1]
        try:
            self.serComm = serial.Serial(self.serialPort, 115200, 8, 'N', 1, timeout=1)
        except:
            print("Serial connection: serial port open error.")
            return None

#-----------------------------------------------------------------------------
    def readComm(self):
        if self.serComm is None: 
            print ("Serial readeing: The sensor is not connected.")
            return None
        output = self.serComm.read(500) # read 500 bytes and parse the data.
        bset = output.split(b'XAKA')    # begine byte of the bytes set.
        for item in bset:
            # 4Bytes*37 = 148 paramters make sure the not data missing.
            if len(item) == 148:
                self.dataList = []
                for idx, data in enumerate(iter(partial(io.BytesIO(item).read, 4), b'')):
                    val = unpack('i', data) if idx == 0 or idx == 1 else unpack(
                        '<f', data)  # get the ID and parameter number
                    self.dataList.append(val[0])
                break # only process the data once.
        if len(self.dataList) == 0: 
            print("Please check the sensor connection.")
            return 0
        print(self.dataList[4])
        return self.dataList[4]


#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
if __name__ == '__main__':
    gv.iCommReader = SensorCom(None)
    print('Start the web server.')
    application.run(debug=False, threaded=True)
    # application.run(host= "0.0.0.0", debug=False, threaded=True) # use 0.0.0.0 if we want access the web from other computer.
    print('Finished')