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

from flask import Flask, render_template, flash, redirect
from testPGlobal import Config

from flask_wtf import FlaskForm # pip install flask-wtf
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

application = Flask(__name__)
application.config.from_object(Config)

@application.route('/')
@application.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)


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



class LoginForm(FlaskForm):
    """ From to handle the login.
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


if __name__ == '__main__':
    application.run(debug=True, threaded=True)