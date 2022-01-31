#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        XAKAsensorComm.py
#
# Purpose:     This module is sensor communication interface module to read the 
#              data from the XAnKA people counting sensor. The user can also use
#              this module to generate the simulation data.
#             
# Author:      Yuancheng Liu
#
# Created:     29/01/2022
# version:     v_2.1
# Copyright:   YC has not added.
# License:     YC has not added.
#-----------------------------------------------------------------------------

import io
import sys
import glob
import serial
import random
from struct import pack, unpack
from functools import partial

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class XandarSimulator(object):
    """ module used to simulate a Xandar COMM USB port interface."""

    def __init__(self, preSavedData=None) -> None:
        self.dataHeader = b''
        self.chunkSize = 100
        self.savedData = preSavedData

    def read(self, byteNum):
        """ return number of bytes simulate the serial read() function."""
        iterN = max(1, byteNum//self.chunkSize)
        dataByte = b''
        for _ in range(iterN):
            data = self.dataHeader + pack('i', 0) + pack('i', random.randint(0, 15))
            for _ in range(35):
                data += pack('f', random.uniform(1.5, 7.0))
                #data += pack('f', float("{:.2f}".format(random.randint(0, 15))))
            dataByte += data
        #print('read: %s' %str(dataByte))
        return dataByte

    def setChunk(self, header, chunkSize):
        self.dataHeader = header
        self.chunkSize = chunkSize

    def write(self, byteData):
        self.savedData = byteData

    def close(self):
        self.savedData = None

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class XAKAsensorComm(object):

    def __init__(self, commPort, simuMd=False) -> None:
        self.serComm = None
        self.serialPort = commPort  # the serial port name we are going to read.
        self.simuMd = simuMd        # simulation mode flag
        self.dataList = []          # current data.

#-----------------------------------------------------------------------------
    def setSerialComm(self, searchFlag=False):
        """ Automatically search for the sensor and do the connection."""
        if not self.serComm is None:
            self.serComm.close()  # close the exists opened port.
            self.serComm = None 
        if self.simuMd:
            print("Load the simulation Xandar sensor comm port.")
            self.serComm = XandarSimulator()
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
                except (OSError, serial.SerialException):
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
            if len(self.dataList) == 0: 
                print("Please check the sensor connection.")
                return None
            else:
                return self.getData()

#-----------------------------------------------------------------------------
    def getData(self):
        return self.dataList

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def testCase(mode=0):
    if mode == 0:
        serComm = XAKAsensorComm('COM0', simuMd=True)
        serComm.setSerialComm()
        print(serComm.fetchSensorData())
        # print(serComm.getData())
    else:
        print("Put your test code here:")
        
#-----------------------------------------------------------------------------
if __name__ == '__main__':
    #testCase()
    testCase(mode=0)
