#-----------------------------------------------------------------------------
# Name:        XandaWebAuth.py
#
# Purpose:     User autherization module used for handle the web site user login
#              signup and logout.
#              
# Author:      Yuancheng Liu
#
# Created:     2022/09/03
# version:     v0.1.5
# Copyright:   Copyright (c) 2024 LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, UserMixin

import XandaGlobal as gv
from ConfigLoader import JsonLoader

auth = Blueprint('auth', __name__)

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
class userMgr(JsonLoader):
    """ User information manager module to handle add user, delete user, update 
        user, query user information. Is is a child module of """
    def __init__(self, userRcd):
        super().__init__()
        self.loadFile(userRcd)

    def userExist(self, userID):
        if not self._haveData(): return False
        if userID in self.jsonData.keys(): return True
        return False

    def getUserInfo(self):
        if self._haveData():
            return self.getJsonData().values()
        return []

    def verifyUser(self, userName, userPwd):
        if self.userExist(userName):
            return self.jsonData[str(userName)]['password'] == userPwd
        return False

    def addUser(self, userName, userPwd, userType, updateRcd=True):
        userName = str(userName).strip()
        if not self._haveData(): return False 
        if self.userExist(userName): return False
        data = {
            "username": str(userName),
            "password": str(userPwd),
            "usertype": str(userType)
        }
        self.jsonData[userName] = data
        if updateRcd: self.updateRcdFile()
        return True
    
    def updatePwd(self, userName, newPwd, updateRcd=True) :
        if self.userExist(userName):
            self.jsonData[userName]['password'] = str(newPwd)
            if updateRcd: self.updateRcdFile()
            return True 
        return False

    def removeUser(self, userName, updateRcd=True):
        print(userName)
        if self.userExist(userName):
            self.jsonData.pop(userName)
            if updateRcd: self.updateRcdFile()
            return True            
        return False

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
# Handle login request.
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
# Handle logout request.
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))