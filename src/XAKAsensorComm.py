#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        XAKAsensorComm.py
#
# Purpose:     This module is sensor communication interface module to read the 
#              data from the Xandar people counting sensor via COM port or GPIO. 
#              The user can also use this module to generate the simulation data.
#             
# Author:      Yuancheng Liu
#
# Created:     29/01/2022
# version:     v_2.3
# Copyright:   Copyright (c) 2024 LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------

import io
import sys
import glob
import serial
import random
import time
import threading

from datetime import datetime
from struct import pack, unpack
from functools import partial
# Current radar data list.
LABEL_LIST = [
    'Seonsor ID: ',
    'Parameter Count:',
    'Presence Info:',
    '0: Sequence',
    '1: Idx People count',
    '2: Reserved',
    '3: Reserved',
    '4: Human Presence',
    '5: Program Version',
    '6: ShortTerm avg',
    '7: LongTerm avg',
    '8: EnvMapping rm T',
    '9: Radar Map rm T',
    '10: Idx for radar mapping',
    '11: Num of ppl for radar map',
    '12: Device ID',
    '13: Start Rng',
    '14: End Rng',
    '15: Reserved',
    '16: LED on/off',
    '17: Trans period',
    '18: Calib factor',
    '19: Tiled Angle',
    '20: Radar Height',
    '21: Avg size',
    '22: Presence on/off',
    '23: Reserved',
    '24: Final ppl num',
    '25: Radar MP val',
    '26: Env MP val',
    '27: serial num_1',
    '28: serial num_2',
    '29: serial dist1',
    '30: serial dist2',
    '31: Reserved',
    '32: Reserved',
    '33: Reserved',
]

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class XandarDataSimulator(object):
    """ Module used to simulate a Xandar COMM USB port interface."""

    def __init__(self, radarId=0, valRange=(1, 7), preSavedData=None) -> None:
        """ Init the data simulator
            Args:
                radarId (int, optional): radar ID. Defaults to 0.
                valRange (tuple, optional): random value range. Defaults to (1.5, 7.0).
                preSavedData (_type_, optional): presaved simulation data. Defaults to None.
        """
        self.dataHeader = b''
        self.radarId = radarId
        self.valRange = valRange
        self.chunkSize = 100
        self.savedData = preSavedData

    #-----------------------------------------------------------------------------
    def read(self, byteNum):
        """ Return number of bytes simulate the serial read() function. return the servial
            communicatin bytes data. 
        """
        iterN = max(1, byteNum//self.chunkSize)
        dataByte = b''
        for _ in range(iterN):
            data = self.dataHeader + pack('i', int(self.radarId)) + pack('i', 34)
            for _ in range(35):
                #data += pack('f', random.uniform(self.valRange[0], self.valRange[1]))
                data += pack('f', round(random.uniform(self.valRange[0], self.valRange[1]), 2))
            dataByte += data
        #print('read: %s' %str(dataByte))
        return dataByte

    #-----------------------------------------------------------------------------
    def setChunk(self, header, chunkSize):
        self.dataHeader = header
        self.chunkSize = chunkSize

    def write(self, byteData):
        self.savedData = byteData

    def close(self):
        self.savedData = None

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class XAKAsensorComm(threading.Thread):
    """ Communication module used to search the radar sensor from serial(COM) port 
        or GPIO then fetch data from the radar. It will running parallel with the 
        main program thread to fetch the data regularly based on user's time interval 
        config setting.
    """

    def __init__(self, commPort, readIntv=2, simuMd=False) -> None:
        """ Constructor.
            Args:
                commPort (str): Serial Port number if not set the module will scan all possible 
                    COM ports to find the connectable one. 
                readIntv (int, optional): data fetch interval in sec. Defaults to 2.
                simuMd (bool, optional): simulation mode. Defaults to False.
        """
        threading.Thread.__init__(self)
        self.serComm = None
        self.serialPort = commPort  # the serial port name we are going to read.
        self.readIntv = readIntv    # radar data read interval in seconds.
        self.simuMd = simuMd        # simulation mode flag
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.dataList = [0]*37          # current data.
        self.terminate = False

#-----------------------------------------------------------------------------
    def setSerialComm(self, searchFlag=False):
        """ Automatically search for the sensor and do the connection."""
        if not self.serComm is None:
            self.serComm.close()  # close the exists opened port.
            self.serComm = None 
        if self.simuMd:
            print("Load the simulation Xandar sensor comm port.")
            self.serComm = XandarDataSimulator()
            self.serComm.setChunk(b'XAKA', 148)
            return True
        portList = []
        if searchFlag and not self.simuMd:
            # look for the port on different platform:
            if sys.platform.startswith('win'):
                ports = ['COM%s' % (i + 1) for i in range(256)]
            elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
                # this excludes your current terminal "/dev/tty"
                ports = glob.glob('/dev/tty[A-Za-z]*')
            elif sys.platform.startswith('darwin'):
                ports = glob.glob('/dev/tty.*')
            else:
                raise EnvironmentError('Serial Port comm connection error: Unsupported platform.')
            for port in ports:
                # Check whether the port can be open.
                try:
                    s = serial.Serial(port)
                    s.close()
                    portList.append(port)
                except Exception as error:
                    pass
            print(('COM connection: the serial port can be used :%s' % str(portList)))
        # normally the first comm prot is resoved by the system.
        #if not self.serialPort in portList: self.serialPort = portList[-1]
        try:
            if not self.serialPort in portList: self.serialPort = portList[-1]
            self.serComm = serial.Serial(self.serialPort, 115200, 8, 'N', 1, timeout=1)
            return True
        except:
            print("Serial connection: serial port open error.")
            return False

#-----------------------------------------------------------------------------
    def fetchSensorData(self):
        """ Fetch data from the sensor and save the data."""
        # load data from the sensor
        if self.serComm is None: 
            print ("Serial reading: The sensor is not connected.")
            return None
        else:
            output = self.serComm.read(500) # read 500 bytes and parse the data.
            bset = output.split(b'XAKA')    # begine byte of the bytes set.
            for item in bset:
                # 4Bytes*37 = 148 paramters make sure the not data missing.
                if len(item) == 148:
                    self.dataList = []
                    for idx, data in enumerate(iter(partial(io.BytesIO(item).read, 4), b'')):
                        val = unpack('i', data) if idx == 0 or idx == 1 else unpack('<f', data)  # get the ID and parameter number
                        self.dataList.append(val[0])
                    break # only process the data once.
            self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if len(self.dataList) == 0: 
                print("Please check the sensor connection.")
                return None
            else:
                return self.getData()

#-----------------------------------------------------------------------------
    def run(self):
        """ Run the sensor comm to fetch the data."""
        print("Start the radar data fetching...")
        while not self.terminate:
            self.fetchSensorData()
            time.sleep(self.readIntv)
        print("Stop the radar data fetching")

#-----------------------------------------------------------------------------
    def getTimestamp(self):
        return self.timestamp

#-----------------------------------------------------------------------------
    def getData(self):
        return self.dataList

    def updateFetchInterval(self, readIntv):
        self.readIntv = max(1, readIntv)

    def stop(self):
        self.terminate = True
        if self.serComm: self.serComm.close()

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def testCase(mode=0):
    if mode == 0:
        print("Test case 1: one time data fetch function.")
        serComm = XAKAsensorComm('COM0', simuMd=True)
        serComm.setSerialComm()
        print(serComm.fetchSensorData())
    elif mode == 1:
        print("Test case 2: continuous data fetch function.")
        serComm = XAKAsensorComm('COM0', simuMd=True)
        serComm.setSerialComm()
        serComm.start()
        time.sleep(3)
        for i in range (10):
            print("- read time: %s" %str(serComm.getTimestamp()))
            datalist = serComm.getData()
            for i, val in enumerate(datalist):
                print("%s : %s" %( LABEL_LIST[i],str(datalist[i])))
            time.sleep(3)
        serComm.stop()
    else:
        print("Put your test code here:")
        
#-----------------------------------------------------------------------------
if __name__ == '__main__':
    #testCase()
    testCase(mode=1)
