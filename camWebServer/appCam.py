#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  	appCam.py
#  	based on tutorial ==> https://blog.miguelgrinberg.com/post/video-streaming-with-flask
# 	PiCam Local Web Server with Flask
# MJRoBot.org 19Jan18

from flask import Flask, render_template, Response,current_app

# Raspberry Pi camera module (requires picamera package)
from camera_pi import Camera

from PIL import Image
import pyzbar.pyzbar as pzb

app = Flask(__name__)


@app.route('/')
def index():
    """Video streaming home page."""
    current_app.logger.warning('this is a log')
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    
    while True:
        
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port =80, debug=True, threaded=True)
