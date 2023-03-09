from flask import Flask, render_template, Response,send_file,request,jsonify
import cv2
import PIL.Image as Image
import base64
from vidgear.gears import CamGear
import csv
import io
import numpy as np
import io
import os,glob
import configparser

def create_sources(s):
    cameras = []
    for ss in s:
        try:
            if ss.isdigit():
                cameras.append(cv2.VideoCapture(int(ss)))
            elif 'youtube' in ss:
                cameras.append(CamGear(source=ss, stream_mode = True, logging=True).start()) # YouTube Video URL as input
            else:  # elif 'rtsp' in ss:
                cameras.append(cv2.VideoCapture(ss))  # use 0 for web camera
                # camera = cv2.VideoCapture('rtsp://freja.hiof.no:1935/rtplive/_definst_/hessdalen03.stream')  # use 0 for web camera
                # for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
        except:
            cameras.append(None)
    return cameras

def get_frame(n):
    global cameras
    try:
        success, frame = cameras[n].read()
    except:
        try:
            frame = cameras[n].read()
            success = True
        except:
            success = False

    if success:
        ret, buffer = cv2.imencode('.jpg', frame)
        data = buffer.tobytes()
        data = base64.b64encode(data).decode()
        msg = 'success'
    else:
        msg = 'can not get frame'
        data = None

    return msg,data

def gen_frames(n):  
    global cameras
    while True:
        try:
            success, frame = cameras[n].read() 
        except:
            try:
                frame = cameras[n].read()
                success = True
            except:
                success = False
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

N_CAMERAS = 12

app = Flask(__name__)

config = configparser.ConfigParser()

dir = 'static/Image'
if not os.path.exists(dir):
    os.makedirs(dir)
for file in os.scandir(dir):
    os.remove(file.path)

detect_data = [-1]*N_CAMERAS

with open('sources.csv') as file:
    sources = file.readlines()
    sources = [x.strip() for x in sources]
cameras = create_sources(sources)

@app.route('/get_frame')
def process():
    data = {}
    for i in range(N_CAMERAS):
        msg,img = get_frame(i)
        data[i] ={
            'msg' : msg,
            'img' : img
        }
    return jsonify(data)

@app.route('/sent_data',methods=['POST'])
def sent_data():
    global detect_data
    print('Recieved from client')
    detect_data = request.data
    detect_data = detect_data.decode("utf-8") 
    detect_data = detect_data.split(',')

    return detect_data

@app.route('/stream')
def index():
    """Video streaming home page."""
    return render_template('stream.html')

@app.route('/setting')
def setting():
    with open('sources.csv') as file:
        numbers = file.readlines()
    numbers = [x.replace('"','') for x in numbers]

    config.read('config.ini')
    model = config.get('model','name')
    print(model,type(model))
    options = []
    for m in ['yolov5n','yolov5s','yolov5m','yolov5l','yolov5x']:
        if m == model:
            options.append(True)
        else:
            options.append(False)
    return render_template('setting.html',number=numbers,option=options)

@app.route('/setting',methods=['POST'])
def setting_submit():
    global cameras

    row_list = []
    for i in range(N_CAMERAS):
        print("[request.form[f'text{i}']]",[request.form[f'text{i}']])
        row_list.append([request.form[f'text{i}']])

    with open('sources.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(row_list)

    with open('sources.csv') as file:
        sources = file.readlines()
        sources = [x.strip() for x in sources]

    dir = 'static/Image'
    for file in os.scandir(dir):
        os.remove(file.path)

    option = request.form['options']

    config.read('config.ini')
    config.set('model', 'name', option)
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

    cameras = create_sources(sources)
    
    return 'setting complete!'

@app.route('/video_feed0')
def video_feed0():
    return Response(gen_frames(0), mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/video_feed1')
def video_feed1():
    return Response(gen_frames(1), mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/video_feed2')
def video_feed2():
    return Response(gen_frames(2), mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/video_feed3')
def video_feed3():
    return Response(gen_frames(3), mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/video_feed4')
def video_feed4():
    return Response(gen_frames(4), mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/video_feed5')
def video_feed5():
    return Response(gen_frames(5), mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/video_feed6')
def video_feed6():
    return Response(gen_frames(6), mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/video_feed7')
def video_feed7():
    return Response(gen_frames(7), mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/video_feed8')
def video_feed8():
    return Response(gen_frames(8), mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/video_feed9')
def video_feed9():
    return Response(gen_frames(9), mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/video_feed10')
def video_feed10():
    return Response(gen_frames(10), mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/video_feed11')
def video_feed11():
    return Response(gen_frames(11), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def process2():
    if os.path.isfile('n_person.csv'):
        with open('n_person.csv') as file:
            n_person = file.readline().split(',')
            # n_person = [int(x.strip()) for x in n_person]
            n_person = [x.strip() for x in n_person]
            n = [int(x.split('|')[0]) for x in n_person]
            t = [x.split('|')[1] for x in n_person]
    else:
        n = [-1]*N_CAMERAS
        t = ['']*N_CAMERAS

    return render_template('index.html',variable=n,variable2=t)

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='0.0.0.0')


