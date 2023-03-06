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
import config

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
model = torch.hub.load('ultralytics/yolov5', config.model)

dir = 'static/Image'
if not os.path.exists(dir):
   os.makedirs(dir)
for file in os.scandir(dir):
    os.remove(file.path)

while True:

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
        

    











#----------------------------------------------------

# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# def sent_sever(a):
#     a = str(a).replace('[','').replace(']','')
#     try:
#         r = requests.post("http://127.0.0.1:5000/sent_data", data=a)
#         return True
#     except:
#         return False


# from io import BytesIO
# import csv

# while True:
#     data = b'48958695427097097402529251103137444756'
#     r = requests.post("http://127.0.0.1:5000/sent_data", data=data)
#     time.sleep(2)

# print('xxx')
# print(type(image))
# print(image)


  
# # path
# path = r'C:\Users\Rajnish\Desktop\geeksforgeeks.png'
  
# # Reading an image in default mode
# image = cv2.imread(path)
  
# # Window name in which image is displayed
# window_name = 'image'
  
# Using cv2.imshow() method
# Displaying the image
# cv2.imshow(window_name, image)
  
# # waits for user to press any key
# # (this is necessary to avoid Python kernel form crashing)
# cv2.waitKey(0)
  
# # closing all open windows
# cv2.destroyAllWindows()

    # with open("imageToSave.png", "wb") as fh:
    #     fh.write(img)

# for (x,y,w,h) in bboxs:
#     cv2.rectangle(frame, (x, y), (x + w, y + h), (255,0,0), 4)
#     cv2.imshow(f"Output Frame", frame)

# frame_b64 = base64.b64encode(frame)

# a = '1,2,3'

# cv2.imshow("image", frame)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

    # if time.time() - start > 2 and sentSever:
    #     sent_sever(p) 
    #     start = time.time()

    # time.sleep(1)
        
    

    

    # time.sleep(2)

    # sentSever = False
