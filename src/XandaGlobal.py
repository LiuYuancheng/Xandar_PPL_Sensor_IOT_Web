#-----------------------------------------------------------------------------
# Name:        XandaGlobal.py
#
# Purpose:     This module is used as a local config file to set global variables
#              which will be used in the other modules.
# Author:      Yuancheng Liu
#
# Created:     2019/07/05 [rebuilt on 29/01/2022]
# version:     v_2.1
# Copyright:   NUS – Singtel Cyber Security Research & Development Laboratory
# License:     YC @ NUS
#-----------------------------------------------------------------------------

import os

print("Current working directory is : %s" % str(os.getcwd()))
dirpath = os.path.dirname(__file__)
print("Current source code location : %s" % dirpath)

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Temporary_secret_key' 

#-------<GLOBAL PARAMTERS>-----------------------------------------------------
iCommReader = None #  Comm port read program.
