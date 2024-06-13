#-----------------------------------------------------------------------------
# Name:        auth.py
#
# Purpose:     User autherization module used for check user login, signup and 
#              logout.
#              
# Author:      Yuancheng Liu
#
# Created:     2022/09/03
# version:     v0.1
# Copyright:   
# License:     
#-----------------------------------------------------------------------------

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, UserMixin

import XandaGlobal as gv

auth = Blueprint('auth', __name__)

#-----------------------------------------------------------------------------
class User(UserMixin):
    """ User object used to get the user info from backend during init.
    Args:
        UserMixin (_type_): _description_
    """
    def __init__(self, id):
        self.id = id
        self.name = id
        self.authority = 0

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.email)

#-----------------------------------------------------------------------------
@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    account = request.form.get('account')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    print((account, password))
    if gv.iUserMgr.userExist(account):
        if gv.iUserMgr.verifyUser(str(account), str(password)):
            login_user(User(account), remember=remember)
            return redirect(url_for('index'))
        else:
            flash('User password incorrect!')
    else:
        flash('Login email address does not exit')
    return redirect(url_for('auth.login'))

#-----------------------------------------------------------------------------
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))