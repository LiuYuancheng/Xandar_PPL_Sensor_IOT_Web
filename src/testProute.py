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

from flask import Flask, render_template
from testPGlobal import Config


application = Flask(__name__)
application.config.from_object(Config)

@application.route('/')
@application.route('/index')
def index():
    user = {'username' : 'test'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        },
        {
            'author': {'username': 'error'},
            'body': 'The Avengers movie was so cool!'
        }

    ]

    return render_template('index.html', title='test', user=user, posts=posts)

if __name__ == '__main__':
    application.run(debug=True, threaded=True)