#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  	appCam.py
#  	based on tutorial ==> https://blog.miguelgrinberg.com/post/video-streaming-with-flask
# 	PiCam Local Web Server with Flask
# MJRoBot.org 19Jan18

from flask import Flask, render_template, Response,current_app,send_from_directory,jsonify

# Raspberry Pi camera module (requires picamera package)
from camera_pi import Camera
import cv2
from PIL import Image
import pyzbar.pyzbar as pzb

app = Flask(__name__)
camera  =  cv2.VideoCapture(0)

@app.route('/')
def index():
    """Video streaming home page."""
    current_app.logger.warning('this is a log')
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    prefix = './imgs/'
    postfix = '.png'
    while True:
        
        sss,img = camera.read()

        
        cv2.imwrite('7.jpg',img)
        ret,jpeg = cv2.imencode('.jpg',img)
        frame = jpeg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    #return send_from_directory('1.jpg')

@app.route('/update-info')
def update_info():
    prefix_f = '请出示二维码'
    img = cv2.imread('7.jpg',cv2.IMREAD_UNCHANGED)
    if not img is None:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        barcodes = pzb.decode(gray)
        if len(barcodes) > 0:
            barcodedata = barcodes[0].data.decode('utf-8')
            return jsonify(message=barcodedata)
    return jsonify(message=prefix_f)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port =80, debug=True, threaded=True)
