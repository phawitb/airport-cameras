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

def create_sources(s):
    cameras = []
    for ss in s:
        if ss.isdigit():
            cameras.append(cv2.VideoCapture(int(ss)))
        elif 'youtube' in ss:
            cameras.append(CamGear(source=ss, stream_mode = True, logging=True).start()) # YouTube Video URL as input
        else:  # elif 'rtsp' in ss:
            cameras.append(cv2.VideoCapture(ss))  # use 0 for web camera
            # camera = cv2.VideoCapture('rtsp://freja.hiof.no:1935/rtplive/_definst_/hessdalen03.stream')  # use 0 for web camera
            # for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera

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

dir = 'static/Image'
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

    return render_template('setting.html',number=numbers)

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
    with open('n_person.csv') as file:
        n_person = file.readline().split(',')
        # n_person = [int(x.strip()) for x in n_person]
        n_person = [x.strip() for x in n_person]
        n = [int(x.split('|')[0]) for x in n_person]
        t = [x.split('|')[1] for x in n_person]

    return render_template('index.html',variable=n,variable2=t)

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0')





#-----------------------------------

# return render_template('setting.html',number=numbers[0],number1=numbers[1],number2=numbers[2])

    # text = [request.form['text']]
    # text1 = [request.form['text1']]
    # text2 = [request.form['text2']]

    # print('processed_text',text,text1,text2)
    # row_list = [text,text1,text2]

# with open('n_person.csv') as file:
    #     n_person = file.readline().split(',')
    #     n_person = [int(x.strip()) for x in n_person]


# @app.route('/capture_video')
# def process2():
#     global cameras,detect_data

#     with open('n_person.csv') as file:
#         n_person = file.readline().split(',')
#         n_person = [int(x.strip()) for x in n_person]

#     with open("0.png", "rb") as image_file:
#         encoded_string = base64.b64encode(image_file.read())
#         encoded_string = encoded_string.decode('utf-8')


#     txt = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">'
#     txt += '<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">'
#     txt += '<title>Live Streaming Demonstration</title></head><body>'
#     txt = '<div class="container"><div class="row"><div class="col-lg-8  offset-lg-2"><h3 class="mt-5">Live Cameras</h3>'
#     for i in range(len(cameras)):
#         msg,data = get_frame(i)
#         if msg == 'success':
#             # txt += f'camera{i+1} n_persons={n_person[i]}<br>'
#             # txt += "<img src='{{url_for('static', filename='0.png')}}' />"
#             # # <img width="300" src="{{url_for("static", filename="0.png")}}">
#             # txt += '<br>'
#             # <img src= "{{url_for('static', filename='/Image/2.png')}}" width="40%"><br>
#             txt += f'camera{i+1} n_persons={n_person[i]}<br><img width="300" src="{{url_for("static", filename="/Image/2.png")}}"><br>'
#             # txt += f'camera{i+1} n_persons={n_person[i]}<br><img width="300" src="data:image/png;base64,{data}"><br>'
#     txt += '</div></div></div></body></html>'
#     return txt


# from PIL import Image

# def gen_frames():  # generate frame by frame from camera
#     # while True:
#     # Capture frame-by-frame
#     success, frame = camera.read()  # read the camera frame
#     if not success:
#         pass
#     else:
#         ret, buffer = cv2.imencode('.jpg', frame)
#         frame = buffer.tobytes()
#         yield (b'--frame\r\n'
#                 b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result



    # return jsonify({
    #            'msg': msg, 
    #            'img': data
    #       })
    # return f'<img src="data:image/png;base64,{data}">'

    # if img:
    #     print(type(img))
    #     img = bytes(img, encoding='utf-8')
    #     img = base64.decodebytes(img)
    #     img = np.array(Image.open(io.BytesIO(img))) 
        # img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # detect_data = img

    # print('Recieved from client')
    # a = request.data
    # print(a,type(a))
    # a = a.decode("utf-8")
    # print(a,type(a))

    # print('Recieved from client: {}'.format(request.data))
    # txt = ''


# def process2():
#     msg,data = get_frame(0)
#     if msg == 'success':
#         return f'<img src="data:image/png;base64,{data}">'

    # success, frame = camera.read()  # read the camera frame
    # if success:
    #     ret, buffer = cv2.imencode('.jpg', frame)
    #     data = buffer.tobytes()
    #     data = base64.b64encode(data).decode()
    
        # return f'<img src="data:image/png;base64,{data}">'

        # Capture frame-by-frame
        # success, frame = cameras[n].read()  # read the camera frame

# cameras = create_sources([0,'https://www.youtube.com/watch?v=DjdUEyjx8GM','https://www.youtube.com/watch?v=cCx8IoIU-6I'])

# camera = cv2.VideoCapture(0)  # use 0 for web camera
# # camera = cv2.VideoCapture('rtsp://freja.hiof.no:1935/rtplive/_definst_/hessdalen03.stream')  # use 0 for web camera
# #  for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
# # for local webcam use cv2.VideoCapture(0)

# cam1 = CamGear(source='https://www.youtube.com/watch?v=DjdUEyjx8GM', stream_mode = True, logging=True).start() # YouTube Video URL as input
# cam2 = CamGear(source='https://www.youtube.com/watch?v=cCx8IoIU-6I', stream_mode = True, logging=True).start() # YouTube Video URL as input

# cameras = [cam1,camera,cam2]
# from flask import Flask, request, jsonify

# @app.route('/processing')
# def process():

#     success, frame = camera.read()  # read the camera frame
#     # if not success:
#     #     pass
#     # else:
#     if success:
#         ret, buffer = cv2.imencode('.jpg', frame)
#         data = buffer.tobytes()

#     # file = request.files['image']
    
#     # img = Image.open(file.stream)
#     # img = img.convert('L')   # ie. convert to grayscale

#     #data = file.stream.read()
#     #data = base64.b64encode(data).decode()
    
#     # buffer = io.BytesIO()
#     # img.save(buffer, 'png')
#     # buffer.seek(0)
    
#     # data = buffer.read()
#     data = base64.b64encode(data).decode()


    
#     return jsonify({
#                'msg': 'success', 
#                'img': data
#           })

#     # return f'<img src="data:image/png;base64,{data}">'

# @app.route('/get_image')
# def get_image():
#     response_pickled = {'scssc':12312}
#     Response(response=response_pickled, status=200, mimetype="application/json")

    # if request.args.get('type') == '1':
    #    filename = 'ok.gif'
    # else:
    #    filename = 'error.gif'
    # filename = 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/1600px-Image_created_with_a_mobile_phone.png'
    # return send_file(filename, mimetype='image/gif')
