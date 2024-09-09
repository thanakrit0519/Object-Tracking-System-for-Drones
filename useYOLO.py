# install opencv "pip install opencv-python" 
# import sys

# sys.path.append('/users/user/appdata/local/packages/pythonsoftwarefoundation.python.3.9_qbz5n2kfra8p0/localcache/local-packages/python39/site-packages')
import cv2 
import time
import math
from ultralytics import YOLO
from controlGimbal import setAngleGimbal
from calLatLong002 import cal_objectGPS2

# distance from camera to object(face) measured 
# centimeter 
Known_distance = 500

# width of face in the real world or Object Plane 
# centimeter 
Known_height = 171

# Colors 
GREEN = (0, 255, 0) 
RED = (0, 0, 255) 
WHITE = (255, 255, 255) 
BLACK = (0, 0, 0) 
BLUE = (255, 0, 0) 

fonts = cv2.FONT_HERSHEY_COMPLEX 

# distance estimation function 
def Distance_finder(k, s, pitch,c): 

	distance = (k*s)*math.cos(pitch) + c

	# return the distance 
	return distance 

def predict(chosen_model, img, conf):
    results = chosen_model(source=img,stream=True)
    return results

def predict_and_detect(chosen_model, img, conf=0.5):
    results = predict(chosen_model, img, conf=conf)
    i=0
    output = []
    for result in results:
        for box in result.boxes:
            # if result.names[int(box.cls[0])] == 'person' or result.names[int(box.cls[0])] == 'car':
            center_w = (int(box.xyxy[0][1]) - int(box.xyxy[0][0]) / 2) + int(box.xyxy[0][0])
            center_h = (int(box.xyxy[0][2]) - int(box.xyxy[0][0]) / 2) + int(box.xyxy[0][0])
            output.append([i,center_w,center_h,int(box.xyxy[0][2]) - int(box.xyxy[0][0])])
            
            cv2.rectangle(img, (int(box.xyxy[0][0]), int(box.xyxy[0][1])),
                        (int(box.xyxy[0][2]), int(box.xyxy[0][3])), BLUE, 2)
            cv2.putText(img, f"{result.names[int(box.cls[0])]} id : {i}",
                        (int(box.xyxy[0][0]), int(box.xyxy[0][1]) - 10),
                        cv2.FONT_HERSHEY_PLAIN, 2, BLUE, 2)
            i+=1
    return img, output

yaw = -45
pitch = 0
# time.sleep(2)
# setAngleGimbal(yaw,pitch)
# time.sleep(4)
model = YOLO("/home/song/CoopProject/trained_model_visdrone2019_1_7_2024/yolov10m.pt")
# cap = cv2.VideoCapture('rtsp://192.168.144.25:8554/video1')
cap = cv2.VideoCapture(0)
frameWidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
frameHeight = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
# # cap.set(cv2.CAP_PROP_FPS,25)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT,360)
print(frameWidth,frameHeight)
# print(cap.get(cv2.CAP_PROP_FPS))
# print(cap.get(cv2.CAP_PROP_FRAME_COUNT))
clat,clon = 13.75,100.5
bearing = 70


track_id = -1
on_track = 0
while True:
    rval, frame = cap.read()
    
    if rval == True:
        img,results = predict_and_detect(model,frame)
        
        if on_track == 1 and len(results) > 0:
            if results[track_id][1] < frameWidth/2 - 20:
                yaw+=0.2
            elif results[track_id][1] > frameWidth/2 + 20:
                yaw-=0.2
            if results[track_id][2] < frameHeight/2 - 20:
                pitch+=0.2
            elif results[track_id][2] > frameHeight/2 + 20:
                pitch-=0.2
            if yaw > 180 :
                yaw = -180 + 0.2
            elif yaw < -180:
                yaw = 180 - 0.2
            # setAngleGimbal(yaw,pitch)
            # Distance = Distance_finder(100, results[track_id][3],pitch,1)
            # lat, lon,_ = cal_objectGPS2(clat, clon, Distance/100, bearing)
            # cv2.line(img, (30, 30), (230, 30), RED, 32) 
            # cv2.line(img, (30, 30), (230, 30), BLACK, 28)
            
            # # Drawing Text on the screen
            # cv2.putText( img, f"Distance: {round(Distance,2)} CM", (30, 35), fonts, 0.6, GREEN, 2)
            # cv2.putText( img, f"Camera lat: {round(clat,6)} Camera lon: {round(clon,6)}", (30, 65), fonts, 0.6, GREEN, 1)
            # cv2.putText( img, f"Object lat: {round(lat,6)} Object lon: {round(lon,6)}", (30, 85), fonts, 0.6, GREEN, 1)
            
        cv2.imshow('video output', img)
        
        inp = cv2.waitKey(1)
        if inp == ord("q"): 
            break
        # elif inp == ord("w"):
        #     pitch+=1
        #     setAngleGimbal(yaw,pitch)
        # elif inp == ord("s"):
        #     pitch-=1
        #     setAngleGimbal(yaw,pitch)
        # elif inp == ord("a"):
        #     yaw-=1
        #     setAngleGimbal(yaw,pitch)
        # elif inp == ord("d"):
        #     yaw+=1
        #     setAngleGimbal(yaw,pitch)
        # elif 48 <= inp <= 57:
        #     track_id = inp - 48
        #     on_track = 1
        # elif inp == ord("x"):
        #     on_track = 0
    # print(yaw,pitch)
		

# closing the camera 
cap.release() 

# closing the windows that are opened 
cv2.destroyAllWindows() 