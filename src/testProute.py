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

import json
import random
import time
from datetime import datetime


from flask import Flask, render_template, flash, redirect, Response
from testPGlobal import Config

from flask_wtf import FlaskForm # pip install flask-wtf
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

import testPGlobal as gv



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

    return render_template('index.html', title='Sign in', user=user, posts=posts)


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

@application.route('/chart')
def chart():
    return render_template('chart.html')

@application.route('/chart-data')
def chart_data():
    def generate_random_data():
        while True:
            json_data = json.dumps(
                {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': random.random() * 100})
            yield f"data:{json_data}\n\n"
            time.sleep(1)

    return Response(generate_random_data(), mimetype='text/event-stream')

class LoginForm(FlaskForm):
    """ From to handle the login.
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

if __name__ == '__main__':
    print('Start the web server.')
    application.run(debug=True, threaded=True)
    print('Finished')