#-----------------------------------------------------------------------------
# Name:        XandaGlobal.py
#
# Purpose:     This module is used as a local config file to set constants, 
#              global parameters which will be used in the other modules.
#              
# Author:      Yuancheng Liu
#
# Created:     2019/07/05 [rebuilt on 30/01/2022]
# version:     v2.3
# Copyright:   Copyright (c) 2022 LiuYuancheng
# License:     MIT License   
#-----------------------------------------------------------------------------
"""
For good coding practice, follow the following naming convention:
    1) Global variables should be defined with initial character 'g'
    2) Global instances should be defined with initial character 'i'
    2) Global CONSTANTS should be defined with UPPER_CASE letters
"""

import os
import sys
import platform

print("Current working directory is : %s" % os.getcwd())
dirpath = os.path.dirname(os.path.abspath(__file__))
print("Current source code location : %s" % dirpath)
APP_NAME = ('XandaPPLRadar', 'IoTWeb')

TOPDIR = 'src'
LIBDIR = 'lib'

idx = dirpath.find(TOPDIR)
gTopDir = dirpath[:idx + len(TOPDIR)] if idx != -1 else dirpath   # found it - truncate right after TOPDIR
# Config the lib folder 
gLibDir = os.path.join(gTopDir, LIBDIR)
if os.path.exists(gLibDir):
    sys.path.insert(0, gLibDir)

#-----------------------------------------------------------------------------
# load the config file.
import ConfigLoader
CONFIG_FILE_NAME = 'Config.txt'
gGonfigPath = os.path.join(dirpath, CONFIG_FILE_NAME)
iConfigLoader = ConfigLoader.ConfigLoader(gGonfigPath, mode='r')
if iConfigLoader is None:
    print("Error: The config file %s is not exist.Program exit!" %str(gGonfigPath))
    exit()
CONFIG_DICT = iConfigLoader.getJson()


APP_SEC_KEY = 'Temporary_secret_key' 
COOKIE_TIME = 30
ADMIN_USER = CONFIG_DICT['ADMIN_USER']

gUser = 'admin'
gPassword = 'admin'

#-------<GLOBAL VARIABLES (start with "g")>-------------------------------------
gTestMd = CONFIG_DICT['TEST_MD']
gAdminPasswd = CONFIG_DICT['ADMIN_PASSWD']


# Flask App parameters : 
gflaskHost = 'localhost' if gTestMd else '0.0.0.0'
gflaskPort = int(CONFIG_DICT['FLASK_SER_PORT']) if 'FLASK_SER_PORT' in CONFIG_DICT.keys() else 5000
gflaskDebug = CONFIG_DICT['FLASK_DEBUG_MD']
gflaskMultiTH =  CONFIG_DICT['FLASK_MULTI_TH']

DE_COMM = 'COM3' if platform.system() == 'Windows' else '/dev/ttyUSB0'


USER_PWD = os.path.join(dirpath, 'ConfigUser.txt')

#-------<GLOBAL PARAMTERS>-----------------------------------------------------
iUserMgr = None
iCommReader = None #  Comm port read program.
