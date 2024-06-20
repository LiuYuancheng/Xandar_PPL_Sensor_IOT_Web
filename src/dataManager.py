#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        dataManager.py [python3]
#
# Purpose:     This module is the data managment module used to link to the DB
#              record file and provide the data to the other modules. 
#
# Author:      Yuancheng Liu
#
# Created:     2024/05/02
# version:     v0.1.2
# Copyright:   Copyright (c) 2024 LiuYuancheng
# License:     MIT License    
#-----------------------------------------------------------------------------

import os
import json

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class userMgr(object):
    """ User Manager class: This class is used to manage the user information."""
    def __init__(self, rcdJsonFilePath):
        """ Load the user record and init the user manager.
            Args:
                rcdJsonFilePath (_type_): _description_
        """
        self.rcdJsonFile = rcdJsonFilePath
        self.userInfo = None
        if os.path.exists(self.rcdJsonFile):
            try:
                with open(self.rcdJsonFile, 'r') as fh:
                    self.userInfo= json.loads(fh.read())
            except Exception as err:
                print("Error to load the user file.")
                return None
        else:
            print("Error: the user file does not exist")
            return None
    
    #-----------------------------------------------------------------------------
    def getUserInfo(self):
        return self.userInfo
    
    def userExist(self, userName):
        if self.userInfo:
            for item in self.userInfo:
                if item['username'] == userName:
                    return True
        return False 

    def verifyUser(self, userName, userPwd):
        if self.userInfo:
            for item in self.userInfo:
                if item['username'] == userName and item['password'] == userPwd: return True
        return False
    
    def updateRcdFile(self):
        with open(self.rcdJsonFile, 'w') as fh:
            fh.write(json.dumps(self.userInfo))

    def addUser(self, userName, userPwd, userType, updateRcd=True):
        if self.userExist(userName): return False
        if self.userInfo:
            data = {
                "username": str(userName),
                "password": str(userPwd),
                "usertype": str(userType)
            }
            self.userInfo.append(data)
            if updateRcd: self.updateRcdFile()
            return True
        return False
    
    def updatePwd(self, userName, newPwd, updateRcd=True) :
        if self.userInfo:
            for idx, item in enumerate(self.userInfo):
                if item['username'] == userName:
                    self.userInfo[idx]['password'] = str(newPwd)
                    break
            if updateRcd: self.updateRcdFile()
            return True
        return False

    def removeUser(self, userName, updateRcd=True):
        print(userName)
        if self.userInfo:
            for idx, item in enumerate(self.userInfo):
                if item['username'] == userName:
                    self.userInfo.pop(idx)
                    print("User %s removed" %str(userName))
                    if updateRcd: self.updateRcdFile()
                    return True            
        return False