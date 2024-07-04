#-----------------------------------------------------------------------------
# Name:        ZmqCfgServer.py
#
# Purpose:     This module is used for a cyber security case study, it will 
#              start a ZMQ server for IoT engineer to user the ZMQ client to 
#              read part of the IoT config data. 
#
# Author:      Yuancheng Liu
#
# Created:     2024/07/03
# version:     v0.0.1
# Copyright:   Copyright (c) 2024 LiuYuancheng
# License:     MIT License   
#-----------------------------------------------------------------------------

import os 
import sys
import zmq
import pickle

print("Current working directory is : %s" % os.getcwd())
dirpath = os.path.dirname(os.path.abspath(__file__))

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

configData = {
    'TEST_MD': CONFIG_DICT['TEST_MD'],
    'RADAR_TYPE': CONFIG_DICT['RADAR_TYPE'],
    'RADAR_PORT': CONFIG_DICT['RADAR_PORT'],
    'RADAR_UPDATE_INTERVAL': CONFIG_DICT['RADAR_UPDATE_INTERVAL'],
    'RPT_MD': CONFIG_DICT['RPT_MD'],
    'RPT_INT': CONFIG_DICT['RPT_INT'],
    'RPT_SER_IP': CONFIG_DICT['RPT_SER_IP'],
    'RPT_SER_PORT': int(CONFIG_DICT['RPT_SER_PORT']),
    'WEB_PORT': CONFIG_DICT['FLASK_SER_PORT'],
}

port = '3003'
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % port)
print("Config Infomation server start, connect port: %s" %str(port))

while True:
    replyData = socket.recv()
    print("Receive the connection data:")
    print(replyData)
    try:
        rspDict = {}
        reqDict = pickle.loads(replyData)
        for key in reqDict.keys():
            if key in configData.keys():
                rspDict[key] = configData[key]
        pickledata = pickle.dumps(rspDict, protocol=pickle.HIGHEST_PROTOCOL)
        socket.send(pickledata)
    except Exception as error:
        print("Error: The data format is not correct! error: %s" % str(error))
        pickledata = pickle.dumps({'Resp': 'Input Error'}, protocol=pickle.HIGHEST_PROTOCOL)
        socket.send(pickledata)
    

