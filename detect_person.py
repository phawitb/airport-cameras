import requests
import json
import cv2
import base64
import numpy as np
import io
import PIL.Image as Image
import time
import pandas as pd
from datetime import datetime
from vidgear.gears import CamGear
import torch
import time
import PIL.Image as Image
import csv
import os,glob
import configparser

def update_mongoDB(i,n_person,now):
    print(f'camera{i} n_person={n_person} time={now}')

def detect_persion(frame):
    results = model(frame)
    df = results.pandas().xyxy[0]
    df = df[df['class']==0]
    bboxs = []
    for index, row in df.iterrows():
        x = int(row['xmin'])
        y = int(row['ymin'])
        w = int(row['xmax']) - int(row['xmin'])
        h = int(row['ymax']) - int(row['ymin'])
        bboxs.append((x,y,w,h))
    n_person = df.shape[0]
    return bboxs,n_person

N_CAMERAS = 12

config = configparser.ConfigParser()

config.read('config.ini')
model_name = config.get('model','name')
model = torch.hub.load('ultralytics/yolov5', model_name)

dir = 'static/Image'
if not os.path.exists(dir):
   os.makedirs(dir)
for file in os.scandir(dir):
    os.remove(file.path)

while True:

    config.read('config.ini')
    if model_name != config.get('model','name'):
        model = torch.hub.load('ultralytics/yolov5', model_name)
        model_name = config.get('model','name')
        print('load new model...',model_name)

    start = time.time()
    try:
        response = requests.get('http://127.0.0.1:5000/get_frame')
        data = json.loads(response.text)
        p = [-1]*12

        for i in data.keys():
            img = data[i]['img']
            msg = data[i]['msg']

            if msg == 'success':
                img = bytes(img, encoding='utf-8')
                img = base64.decodebytes(img)
                img = np.array(Image.open(io.BytesIO(img))) 
                frame = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

                now = datetime.now()
                bboxs,n_person = detect_persion(frame)

                for (x,y,w,h) in bboxs:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255,0,0), 4)
                    # cv2.imshow(f"Output Frame", frame)
                cv2.imwrite(f'static/Image/{i}.png', frame)

                p[int(i)] = f"{n_person}|{now}"

                update_mongoDB(i,n_person,now)   #update mongoDB------------------
            else:
                try:
                    os.remove(f'static/Image/{i}.png')
                except:
                    pass
                p[int(i)] = f"-1|{now}"
                print(f'camera{i} error!!')

        with open('n_person.csv', 'w') as f:
            write = csv.writer(f)
            write.writerow(p)

        print(f'loop time={time.time()-start} s')

    except:
        print('Can not find sever!')
        time.sleep(1)
        
