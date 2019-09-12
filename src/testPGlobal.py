#-----------------------------------------------------------------------------
# Name:        firmwGlobal.py
#
# Purpose:     This module is used set the Local config file as global value 
#              which will be used in the other modules.
# Author:      Yuancheng Liu
#
# Created:     2019/05/17
# Copyright:   NUS – Singtel Cyber Security Research & Development Laboratory
# License:     YC @ NUS
#-----------------------------------------------------------------------------
import os

dirpath = os.getcwd()
print("testProute: Current working directory is : %s" %dirpath)


#-------<GLOBAL PARAMTERS>-----------------------------------------------------
iCommReader = None

