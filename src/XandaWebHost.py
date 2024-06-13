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
from flask import Flask, render_template, flash, url_for, redirect, request, Response
from flask_wtf import FlaskForm # pip install flask-wtf
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_login import LoginManager, login_required

import XandaGlobal as gv
import XandaWebAuth
import XAKAsensorComm as xcomm
import dataManager as dm


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
    
    # Init the user manager
    gv.iUserMgr = dm.userMgr(gv.gUsersRcd)

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


#-----------------------------------------------------------------------------
# admin user account's request handling function.
@application.route('/accmgmt')
@login_required
def accmgmt():
    users = gv.iUserMgr.getUserInfo()
    return render_template('accmgmt.html', posts=users)

@application.route('/accmgmt/<string:username>/<string:action>', methods=('POST',))
@login_required
def changeAcc(username, action):
    if action == 'delete':
        if gv.iUserMgr.removeUser(str(username)):
            flash('User deleted.')
        else:
            flash('User not found.')
    return redirect(url_for('accmgmt'))


@application.route('/addnewuser', methods=['POST', ])
@login_required
def addnewuser():
    if request.method == 'POST':
        tgttype = request.form.getlist('optradio')
        tgtUser = request.form.get("username")
        tgtPwd = request.form.get("password")

        print((tgttype, tgtUser, tgtPwd))
        
        if not gv.iUserMgr.userExist(tgtUser):
            userType = 'admin' if 'option1' in tgttype else 'user'
            if gv.iUserMgr.addUser(tgtUser, tgtPwd, userType):
                flash('User %s has been added.' %str(tgtUser))
            else:
                flash('User %s can not be added.' %str(tgtUser))
        else:
            flash('User %s has been exist.' %str(tgtUser))
    return redirect(url_for('accmgmt'))

#-----------------------------------------------------------------------------
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

@application.route('/chart-data') # the route component must match the related <dev> in the html file.
@login_required
def chart_data():
    def generateSensorData():
        while True:
            dataList = gv.iCommReader.fetchSensorData()
            peopleNum = int(dataList[27])
            json_data = json.dumps({'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': peopleNum })
            #print(f"data:{json_data}\n\n")
            yield "data:%s\n\n" %str(json_data)
            time.sleep(gv.gRadarUpdateInterval)
    return Response(generateSensorData(), mimetype='text/event-stream')











#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
if __name__ == '__main__':
    # application.run(host= "0.0.0.0", debug=False, threaded=True) # use 0.0.0.0 if we want access the web from other computer.
    application.run(host=gv.gflaskHost,
                port=gv.gflaskPort,
                debug=gv.gflaskDebug,
                threaded=gv.gflaskMultiTH)
