#-----------------------------------------------------------------------------
# Name:        XandaGlobal.py
#
# Purpose:     This module is used as a local config file to set global variables
#              which will be used in the other modules.
# Author:      Yuancheng Liu
#
# Created:     2019/07/05 [rebuilt on 30/01/2022]
# version:     v_2.1
# Copyright:   NUS – Singtel Cyber Security Research & Development Laboratory
# License:     YC @ NUS
#-----------------------------------------------------------------------------

import os
import platform

print("Current working directory is : %s" % str(os.getcwd()))
dirpath = os.path.dirname(__file__)
print("Current source code location : %s" % dirpath)

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Temporary_secret_key' 

DE_COMM = 'COM3' if platform.system() == 'Windows' else '/dev/ttyUSB0'


USER_PWD = os.path.join(dirpath, 'ConfigUser.txt')

#-------<GLOBAL PARAMTERS>-----------------------------------------------------
iUserMgr = None
iCommReader = None #  Comm port read program.


gSimulationMode = True