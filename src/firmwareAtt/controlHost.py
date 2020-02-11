#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        attackHost.py [python2.7/python3]
#
# Purpose:     This module is used to create a flask server to do the firmware
#              upload and attestation.
# Author:      Yuancheng Liu
#
# Created:     2020/01/29
# Copyright:   YC @ Singtel Cyber Security Research & Development Laboratory
# License:     YC
#-----------------------------------------------------------------------------
import os
import random
import time
import socket
from flask import Flask, redirect, url_for, request, flash, render_template, Response, jsonify
from werkzeug.utils import secure_filename


import globalVal as gv
import sensorPatt as sp

TEST_MODE = True # Test mode flag - True: test on local computer
SEV_IP = ('127.0.0.1', 5006) if TEST_MODE else ('192.168.10.244', 5006)
BUFFER_SZ = 1024
UPLOAD_FOLDER = os.getcwd()

# Init the UDP send server
crtClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

class webHandler(object):
    """ handler class to handle differetn web function.""" 
    def __init__(self, parent):
        self.parent = parent
        self.extenction = ('bin')

    def allowed_file(self, filename):
	    return '.' in filename and filename.split('.')[-1].lower() in self.extenction

    def fileUpload(self, request):
        
        if 'file' not in request.files:
            flash('No file part')
            return request.url
        fh = request.files['file']
        if fh.filename == '':
            flash('No file selected for uploading')
            return request.url
        elif fh and self.allowed_file(fh.filename):
            filename = secure_filename(fh.filename)
            fh.save(gv.FM_FILE)
            flash('File successfully uploaded')
            return '/'
        else:
            flash('Allowed file types are bin')
            return request.url

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

# Init the flask web server program and rout the function.
app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
gv.iRouteHandler = webHandler(app)
gv.iSensorThread = sp.SensorPatt(app, 0, "Arduino_ESP8266", 1)
gv.iSensorThread.start()

@app.route('/')
def index():
    # Add CSS in the html for flask is shown in this link: 
    # https://pythonhow.com/add-css-to-flask-website/
    return render_template('index.html')

#rendering the HTML page which has the button
@app.route('/json')
def json():
    return render_template('index.html')

#Start the gateway encryption.
@app.route('/enableEncrypt')
def startAtt1():
    print ("Start the gateway encryption.")
    if request.method == 'GET':
        msg = 'T;1'
        crtClient.sendto(msg.encode('utf-8'), SEV_IP)
    return ("nothing")

#Disable the gateway encryption
@app.route('/disableEncrypt')
def stopAtt1():
    print ("Disable the gateway encryption")
    if request.method == 'GET':
        msg = 'T;0'
        crtClient.sendto(msg.encode('utf-8'), SEV_IP)
    return ("nothing")

# Start the key exchange
@app.route('/exchangeKey')
def startAtt2():
    print ("Start the key exchange.")
    if request.method == 'GET':
        msg = 'T;2'
        crtClient.sendto(msg.encode('utf-8'), SEV_IP)
    return ("nothing")



@app.route('/', methods=['POST'])
def upload_file():
    """ https://www.roytuts.com/python-flask-file-upload-example/
    """
    if request.method == 'POST':
    # check if the post request has the file part 
        return redirect(gv.iRouteHandler.fileUpload(request))

@app.route('/progress')
def progress():
	def generate():
		x = 0
		while x <= 100:
			yield "data:" + str(x) + "\n\n"
			x = x + 10
			time.sleep(0.5)
	return Response(generate(), mimetype= 'text/event-stream')



if __name__ == '__main__':
    app.run(host= "0.0.0.0", debug=False, threaded=True)
   