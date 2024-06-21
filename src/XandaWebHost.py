#------------------------------------------------------------------------------
# Name:        XandaWebHost.py
#
# Purpose:     Flask website host IoT frame work program running on the Raspberry-PI
#              to read the Xanda people detection radar information, then display
#              the information on web interface. It also provide the users managment
#              feature, radar configuration adjustment and interface for other
#              program to fetch the information from the IoT
#
# Author:      Yuancheng Liu
#
# Created:     2019/09/11 
# version:     v2.3 [rebuilt from v1.5 on 15/06/2024 ]
# Copyright:   Copyright (c) 2024 LiuYuancheng
# License:     MIT License
#------------------------------------------------------------------------------
""" 
    Program design:
        We want to provide a simple frame work program which can run on a Raspberry-PI
        to make it to be a IoT device. The frame work will provide a web interface for: 
        1. sensor data access authorization and the user management. 
        2. configure the setting of sensor which connected to Raspberry-PI.
        3. Interface for IoT Hub to fetch the data or report the data to IoT hub.
"""

import json
import time
from datetime import datetime, timedelta

# import flask module to create the server.
from flask import Flask, render_template, flash, url_for, redirect, request, Response
from flask_login import LoginManager, login_required

import XandaGlobal as gv
import XandaWebAuth
import XAKAsensorComm as xcomm

# -----------------------------------------------------------------------------
# Init the flask web app program.
def createApp():
    """ Create the flask App."""
    # init the web host
    app = Flask(__name__)
    app.config['SECRET_KEY'] = gv.APP_SEC_KEY
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=gv.COOKIE_TIME)
    from XandaWebAuth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # Create the user login manager
    loginMgr = LoginManager()
    loginMgr.loginview = 'auth.login'
    loginMgr.init_app(app)

    @loginMgr.user_loader
    def loadUser(userID):
        return XandaWebAuth.User(userID)
    return app

# Init the user manager
gv.iUserMgr = XandaWebAuth.userMgr(gv.gUsersRcd)
# Init the radar communication module

gv.iCommReader = xcomm.XAKAsensorComm(gv.DE_COMM, readIntv=gv.gRadarUpdateInterval, simuMd=gv.gTestMd)
searchRadar = not gv.gTestMd
gv.iCommReader.setSerialComm(searchFlag=searchRadar)
gv.iCommReader.start()
application = createApp()

# -----------------------------------------------------------------------------
# page 0: index page
@application.route('/')
@application.route('/index')
def index():
    return render_template('index.html')

# -----------------------------------------------------------------------------
# page 1: sensor data access page
@application.route('/chart')
@login_required
def chart():
    posts = {'page': 1,
             'radarType': gv.gRadarType,
             'radarPort': gv.gRadarPort,
             'radarConn': gv.gTestMd,
             'radarInt': str(gv.gRadarUpdateInterval)
             }
    return render_template('chart.html', posts=posts)

# the route component must match the related <dev> in the html file.
@application.route('/chart-data')
@login_required
def chart_data():
    def generateSensorData():
        while True:
            timestamp = gv.iCommReader.getTimestamp()
            dataList = gv.iCommReader.getData()
            peopleNum = int(dataList[27])
            json_data = json.dumps({'time': timestamp, 'value': peopleNum})
            # print(f"data:{json_data}\n\n")
            yield "data:%s\n\n" % str(json_data)
            time.sleep(gv.gRadarUpdateInterval)
    return Response(generateSensorData(), mimetype='text/event-stream')

# -----------------------------------------------------------------------------
# page 2 admin user account's request handling function.
@application.route('/accmgmt')
@login_required
def accmgmt():
    posts = {'page': 2,
             'users': gv.iUserMgr.getUserInfo()
            }
    return render_template('accmgmt.html', posts=posts)

@application.route('/accmgmt/<string:username>/<string:action>', methods=('POST',))
@login_required
def changeAcc(username, action):
    """ Handle the user account's POST request.
        Args:
            username (str): user name string
            action (str): action tag.
    """
    if action == 'delete':
        if gv.iUserMgr.removeUser(str(username).strip()):
            flash('User %s deleted.' % str(username))
        else:
            flash('User not found.')
    return redirect(url_for('accmgmt'))

@application.route('/addnewuser', methods=['POST', ])
@login_required
def addnewuser():
    """ Addd a new user in the IoT system."""
    if request.method == 'POST':
        tgttype = request.form.getlist('optradio')
        tgtUser = request.form.get("username")
        tgtPwd = request.form.get("password")
        # print((tgttype, tgtUser, tgtPwd))
        if not gv.iUserMgr.userExist(tgtUser):
            userType = 'admin' if 'option1' in tgttype else 'user'
            if gv.iUserMgr.addUser(tgtUser, tgtPwd, userType):
                flash('User %s has been added.' % str(tgtUser))
            else:
                flash('User %s can not be added.' % str(tgtUser))
        else:
            flash('User %s has been exist.' % str(tgtUser))
    return redirect(url_for('accmgmt'))

@application.route('/setpassword/<string:username>', methods=['POST', ])
@login_required
def setpassword(username):
    """ Update the user password."""
    if request.method == 'POST':
        newPassword = str(request.form.get("newpassword")).strip()
        if newPassword:
            rst = gv.iUserMgr.updatePwd(username, newPassword)
            if rst:
                flash('Password of user %s has been changed.' % str(username))
            else:
                flash('Password of user %s can not be changed.' % str(username))
        else:
            flash('Password can not be empty.')
    return redirect(url_for('accmgmt'))

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    # application.run(host= "0.0.0.0", debug=False, threaded=True) # use 0.0.0.0 if we want access the web from other computer.
    application.run(host=gv.gflaskHost,
                    port=gv.gflaskPort,
                    debug=gv.gflaskDebug,
                    threaded=gv.gflaskMultiTH)
