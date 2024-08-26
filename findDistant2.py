# install opencv "pip install opencv-python" 
# import sys

# sys.path.append('/users/user/appdata/local/packages/pythonsoftwarefoundation.python.3.9_qbz5n2kfra8p0/localcache/local-packages/python39/site-packages')
import math as Math
import cv2 
import socket
import sys
import time
from ultralytics import YOLO
import controlGimbal

# distance from camera to object(face) measured 
# centimeter 
Known_distance = 50

# width of face in the real world or Object Plane 
# centimeter 
Known_width = 14.28

# Colors 
GREEN = (0, 255, 0) 
RED = (0, 0, 255) 
WHITE = (255, 255, 255) 
BLACK = (0, 0, 0) 
BLUE = (255, 0, 0) 


# focal length finder function 
def Focal_Length_Finder(measured_distance, real_width, width_in_rf_image): 

	# finding the focal length 
	focal_length = (width_in_rf_image * measured_distance) / real_width 
	return focal_length 

# distance estimation function 
def Distance_finder(Focal_Length, real_face_width, face_width_in_frame): 

	distance = (real_face_width * Focal_Length)/face_width_in_frame

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
            if result.names[int(box.cls[0])] == 'person' or result.names[int(box.cls[0])] == 'car':
                center_w = (int(box.xyxy[0][1]) - int(box.xyxy[0][0]) / 2) + int(box.xyxy[0][0])
                center_h = (int(box.xyxy[0][2]) - int(box.xyxy[0][0]) / 2) + int(box.xyxy[0][0])
                output.append([i,center_w,center_h])
                
                cv2.rectangle(img, (int(box.xyxy[0][0]), int(box.xyxy[0][1])),
                            (int(box.xyxy[0][2]), int(box.xyxy[0][3])), BLUE, 2)
                cv2.putText(img, f"{result.names[int(box.cls[0])]} id : {i}",
                            (int(box.xyxy[0][0]), int(box.xyxy[0][1]) - 10),
                            cv2.FONT_HERSHEY_PLAIN, 2, BLUE, 2)
                i+=1
    return img, output


# reading reference_image from directory 
# ref_image = cv2.imread("/home/song/CoopProject/Ref_image.jpg") 

# find the face width(pixels) in the reference_image 

# get the focal by calling "Focal_Length_Finder" 
# face width in reference(pixels), 
# Known_distance(centimeters), 
# known_width(centimeters) 
# Focal_length_found = Focal_Length_Finder( 
# 	Known_distance, Known_width, ref_image_face_width) 

# print(Focal_length_found) 

# show the reference image 
# cv2.imshow("ref_image", ref_image)

# initialize the camera object so that we 
# can get frame from it 
# cap = cv2.VideoCapture("rtsp://192.168.144.25:8554/video1") 
yaw = -45
pitch = 0
time.sleep(2)
controlGimbal.setAngleGimbal(yaw,pitch)
time.sleep(4)
model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture('rtsp://192.168.144.25:8554/video1')
frameWidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
frameHeight = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
# # cap.set(cv2.CAP_PROP_FPS,25)
print(frameWidth,frameHeight)
# print(cap.get(cv2.CAP_PROP_FPS))
# print(cap.get(cv2.CAP_PROP_FRAME_COUNT))
clat,clon = 13.75,100.5
bearing = 70


track_id = -1
on_track = 0
while True:
    rval, frame = cap.read()
    
    # if face_width_in_frame != 0:
    #     Distance = Distance_finder(Focal_length_found, Known_width, face_width_in_frame)
        
    #     lat, lon = destinationPoint(clat, clon, Distance/100, bearing)
        
    #     # draw line as background of text
    #     cv2.line(frame, (30, 30), (230, 30), RED, 32) 
    #     cv2.line(frame, (30, 30), (230, 30), BLACK, 28)
        
    #     # Drawing Text on the screen
    #     cv2.putText( frame, f"Distance: {round(Distance,2)} CM", (30, 35), fonts, 0.6, GREEN, 2)
    #     cv2.putText( frame, f"Camera lat: {round(clat,6)} Camera lon: {round(clon,6)}", (30, 65), fonts, 0.6, GREEN, 1)
    #     cv2.putText( frame, f"Object lat: {round(lat,6)} Object lon: {round(lon,6)}", (30, 85), fonts, 0.6, GREEN, 1)
        
    #     # show the frame on the screen 
    # cv2.imshow("frame", frame) 
    
    if rval == True:
        img,results = predict_and_detect(model,frame)
        cv2.imshow('video output', img)
        
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
            controlGimbal.setAngleGimbal(yaw,pitch)
        
        inp = cv2.waitKey(1)
        if inp == ord("q"): 
            break
        elif inp == ord("w"):
            pitch+=1
            controlGimbal.setAngleGimbal(yaw,pitch)
        elif inp == ord("s"):
            pitch-=1
            controlGimbal.setAngleGimbal(yaw,pitch)
        elif inp == ord("a"):
            yaw-=1
            controlGimbal.setAngleGimbal(yaw,pitch)
        elif inp == ord("d"):
            yaw+=1
            controlGimbal.setAngleGimbal(yaw,pitch)
        elif 48 <= inp <= 57:
            track_id = inp - 48
            on_track = 1
        elif inp == ord("x"):
            on_track = 0
    # print(yaw,pitch)
		

# closing the camera 
cap.release() 

# closing the windows that are opened 
cv2.destroyAllWindows() 