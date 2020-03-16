#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        tcpStream.py
#
# Purpose:     This module will create a tcp stream server for the raspberry PI
#              camera. vlc tcp/h264://my_pi_address:8000/
#              
# Author:       Yuancheng Liu
#
# Created:     2020/03/16
# Copyright:   YC @ Singtel Cyber Security Research & Development Laboratory
# License:     YC
#-----------------------------------------------------------------------------

import socket
import time
import picamera

PLAY_TIME = 60 # time(seconds) 


camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 24

server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)

# vlc tcp/h264://my_pi_address:8000/
# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('wb')
try:
    camera.start_recording(connection, format='h264')
    camera.wait_recording(60)
    camera.stop_recording()
finally:
    connection.close()
    server_socket.close()