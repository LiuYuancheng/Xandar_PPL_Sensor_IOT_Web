#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        threats2MitreApp.py [python3]
#
# Purpose:     This module is the main web interface to call the AI-llm MITRE 
#              ATT&CK-Mapper/ CWE-Matcher module to generate the related report.
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

class userMgr(object):

    def __init__(self, rcdJsonFilePath):
        self.rcdJsonFile = rcdJsonFilePath
        self.userInfo = None
        if os.path.exists(self.rcdJsonFile):
            try:
                with open(self.rcdJsonFile, 'r') as fh:
                    self.userInfo= json.loads(fh.read())
            except Exception as err:
                print("Error to load the user file")
                return None
        else:
            print("Error: the user file does not exist")
            return None
    
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

    def addUser(self, userName, userPwd, userType, updateRcd=False):
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
    
    def updatePwd(self, userName, newPwd, updateRcd=False) :
        if self.userInfo:
            for idx, item in enumerate(self.userInfo):
                if item['username'] == userName:
                    self.userInfo[idx]['password'] = str(newPwd)
                    break
            if updateRcd: self.updateRcdFile()
            return True
        return False

    def removeUser(self, userName, updateRcd=False):
        if self.userInfo:
            for idx, item in enumerate(self.userInfo):
                if item['username'] == userName:
                    self.userInfo.pop(idx)
                break
            if updateRcd: self.updateRcdFile()
            return True
        return False