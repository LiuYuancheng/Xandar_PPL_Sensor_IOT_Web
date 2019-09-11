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

from flask import Flask, render_template

application = Flask(__name__)

@application.route('/')
@application.route('/index')
def index():
    user = {'username' : 'test'}
    return render_template('index.html', title='test', user=user)

if __name__ == '__main__':
    application.run(debug=True, threaded=True)