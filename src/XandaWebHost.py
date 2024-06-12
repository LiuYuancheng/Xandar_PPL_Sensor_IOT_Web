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



import time
from datetime import datetime, timedelta
from threading import Thread



from struct import unpack
from datetime import datetime
from functools import partial
# import flask module to create the server.
from flask import Flask, render_template, flash, redirect, Response
from flask_wtf import FlaskForm # pip install flask-wtf
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_login import LoginManager, login_required

import XandaGlobal as gv
import XandaWebAuth
import XAKAsensorComm as xcomm


#-----------------------------------------------------------------------------
# Init the flask web app program.
def createApp():
    """ Create the flask App."""
    # init the web host
    app = Flask(__name__)
    app.config['SECRET_KEY'] = gv.APP_SEC_KEY
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=gv.COOKIE_TIME)
    from XandaWebAuth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    gv.iCommReader = xcomm.XAKAsensorComm(gv.DE_COMM, simuMd=gv.gTestMd)
    gv.iCommReader.setSerialComm(searchFlag=True)

    # Create the user login manager
    loginMgr = LoginManager()
    loginMgr.loginview = 'auth.login'
    loginMgr.init_app(app)
    @loginMgr.user_loader
    def loadUser(userID):
        return XandaWebAuth.User(userID)
    return app

application = createApp()

#-----------------------------------------------------------------------------
@application.route('/')
@application.route('/index')
def index():
    return render_template('index.html')

@application.route('/chart')
def chart():
    posts = {'page': 1}
    return render_template('chart.html', posts=posts)


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
    # application.run(host= "0.0.0.0", debug=False, threaded=True) # use 0.0.0.0 if we want access the web from other computer.
    application.run(host=gv.gflaskHost,
                port=gv.gflaskPort,
                debug=gv.gflaskDebug,
                threaded=gv.gflaskMultiTH)
