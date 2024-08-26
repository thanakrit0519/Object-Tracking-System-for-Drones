# install opencv "pip install opencv-python" 
# import sys

# sys.path.append('/users/user/appdata/local/packages/pythonsoftwarefoundation.python.3.9_qbz5n2kfra8p0/localcache/local-packages/python39/site-packages')
import math as Math
import cv2 
import socket
import sys
import time
from ultralytics import YOLO

RECV_BUUF_SIZE = 64
SERVER_PORT = 37260          # Gimbal Camera (Server) Port
SERVER_IP = "192.168.144.25" # Gimbal Camera (Server) IP Addresses

crc16_tab = [
    0x0, 0x1021, 0x2042, 0x3063, 0x4084, 0x50a5, 0x60c6, 0x70e7, 
    0x8108, 0x9129, 0xa14a, 0xb16b, 0xc18c, 0xd1ad, 0xe1ce, 0xf1ef,
    0x1231, 0x210, 0x3273, 0x2252, 0x52b5, 0x4294, 0x72f7, 0x62d6,
    0x9339, 0x8318, 0xb37b, 0xa35a, 0xd3bd, 0xc39c, 0xf3ff, 0xe3de,
    0x2462, 0x3443, 0x420, 0x1401, 0x64e6, 0x74c7, 0x44a4, 0x5485,
    0xa56a, 0xb54b, 0x8528, 0x9509, 0xe5ee, 0xf5cf, 0xc5ac, 0xd58d,
    0x3653, 0x2672, 0x1611, 0x630, 0x76d7, 0x66f6, 0x5695, 0x46b4,
    0xb75b, 0xa77a, 0x9719, 0x8738, 0xf7df, 0xe7fe, 0xd79d, 0xc7bc,
    0x48c4, 0x58e5, 0x6886, 0x78a7, 0x840, 0x1861, 0x2802, 0x3823,
    0xc9cc, 0xd9ed, 0xe98e, 0xf9af, 0x8948, 0x9969, 0xa90a, 0xb92b,
    0x5af5, 0x4ad4, 0x7ab7, 0x6a96, 0x1a71, 0xa50, 0x3a33, 0x2a12,
    0xdbfd, 0xcbdc, 0xfbbf, 0xeb9e, 0x9b79, 0x8b58, 0xbb3b, 0xab1a,
    0x6ca6, 0x7c87, 0x4ce4, 0x5cc5, 0x2c22, 0x3c03, 0xc60, 0x1c41,
    0xedae, 0xfd8f, 0xcdec, 0xddcd, 0xad2a, 0xbd0b, 0x8d68, 0x9d49,
    0x7e97, 0x6eb6, 0x5ed5, 0x4ef4, 0x3e13, 0x2e32, 0x1e51, 0xe70,
    0xff9f, 0xefbe, 0xdfdd, 0xcffc, 0xbf1b, 0xaf3a, 0x9f59, 0x8f78,
    0x9188, 0x81a9, 0xb1ca, 0xa1eb, 0xd10c, 0xc12d, 0xf14e, 0xe16f,
    0x1080, 0xa1, 0x30c2, 0x20e3, 0x5004, 0x4025, 0x7046, 0x6067,
    0x83b9, 0x9398, 0xa3fb, 0xb3da, 0xc33d, 0xd31c, 0xe37f, 0xf35e,
    0x2b1, 0x1290, 0x22f3, 0x32d2, 0x4235, 0x5214, 0x6277, 0x7256,
    0xb5ea, 0xa5cb, 0x95a8, 0x8589, 0xf56e, 0xe54f, 0xd52c, 0xc50d,
    0x34e2, 0x24c3, 0x14a0, 0x481, 0x7466, 0x6447, 0x5424, 0x4405,
    0xa7db, 0xb7fa, 0x8799, 0x97b8, 0xe75f, 0xf77e, 0xc71d, 0xd73c,
    0x26d3, 0x36f2, 0x691, 0x16b0, 0x6657, 0x7676, 0x4615, 0x5634,
    0xd94c, 0xc96d, 0xf90e, 0xe92f, 0x99c8, 0x89e9, 0xb98a, 0xa9ab,
    0x5844, 0x4865, 0x7806, 0x6827, 0x18c0, 0x8e1, 0x3882, 0x28a3,
    0xcb7d, 0xdb5c, 0xeb3f, 0xfb1e, 0x8bf9, 0x9bd8, 0xabbb, 0xbb9a,
    0x4a75, 0x5a54, 0x6a37, 0x7a16, 0xaf1, 0x1ad0, 0x2ab3, 0x3a92,
    0xfd2e, 0xed0f, 0xdd6c, 0xcd4d, 0xbdaa, 0xad8b, 0x9de8, 0x8dc9,
    0x7c26, 0x6c07, 0x5c64, 0x4c45, 0x3ca2, 0x2c83, 0x1ce0, 0xcc1,
    0xef1f, 0xff3e, 0xcf5d, 0xdf7c, 0xaf9b, 0xbfba, 0x8fd9, 0x9ff8,
    0x6e17, 0x7e36, 0x4e55, 0x5e74, 0x2e93, 0x3eb2, 0xed1, 0x1ef0
]

def CRC16_cal(ptr):
    crc = 0
    for i in ptr:
        temp = (crc >> 8) & 0xff
        oldcrc16 = crc16_tab[i ^ temp]
        crc = (crc << 8) ^ oldcrc16
    return crc & 0x00000000000000000ffff

def tohex(val, nbits):
    return hex((val + (1 << nbits)) % (1 << nbits))

def destinationPoint(lat1, lon1, distance, bearing, radius=6371e3):

    δ = distance / radius  # angular distance in radians
    θ = bearing / 180 * Math.pi

    lat1 = lat1 / 180 * Math.pi
    lon1 = lon1 / 180 * Math.pi

    sinlat2 = Math.sin(lat1) * Math.cos(δ) + Math.cos(lat1) * Math.sin(δ) * Math.cos(θ)
    lat2 = Math.asin(sinlat2)
    y = Math.sin(θ) * Math.sin(δ) * Math.cos(lat1)
    x = Math.cos(δ) - Math.sin(lat1) * sinlat2
    lon2 = lon1 + Math.atan2(y, x)

    lat = lat2 * 180 / Math.pi
    lon = lon2 * 180 / Math.pi

    lon = (lon + 540) % 360 - 180

    return lat, lon

def setAngleGimbal(yaw,pitch):
    yaw = yaw*10
    pitch = pitch *10
    try:
        sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error as e:
        print(f"socket error: {e}")
        sys.exit(1)

    # Set IP addresses and port number of gimbal camera
    
    send_addr = (SERVER_IP, SERVER_PORT)
    #data = '55 66 01 02 00 00 00 0e 00 00'
    yaw = tohex(yaw,16)
    pitch = tohex(pitch,16)

    #print(yaw,pitch)
    yaw=int(yaw,16)
    yaw1 = yaw//(16*16)
    yaw2 = yaw%(16*16)

    pitch=int(pitch,16)
    pitch1 = pitch//(16*16)
    pitch2 = pitch%(16*16)
    
    data = [0x55,0x66,0x01,0x04,0x00,0x00,0x00,0x0e,yaw2,yaw1,pitch2,pitch1]
    # data = [0x55,0x66,0x01,0x00,0x00,0x00,0x00,0x0d]
    crc=CRC16_cal(data)
    print(hex(crc))
    data.append(crc&0x00ff)
    data.append(crc>>8)
    print(data)
    send_buf = bytearray(data)  # Frame protocol of the relevant functions in hexadecimal

    # Send frame data
    print("Send HEX data")
    try:
        sockfd.sendto(send_buf, send_addr)
    except socket.error as e:
        print(f"sendto error: {e}")
        sys.exit(1)

    # Receive the responding data from gimbal camera
    recv_buf, addr = sockfd.recvfrom(RECV_BUUF_SIZE)

    # print the received data in hexadecimal
    print("Received HEX data: ", end="")
    for byte in recv_buf:
        print(f"{byte:02x} ", end="")
    print()

    # close socket
    sockfd.close()
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

# def face_data(image):
#     face_width = 0 # making face width to zero
#     centerX = 0
#     centerY = 0
#     # converting color image to gray scale image
#     gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
#     faces = face_cascade.detectMultiScale(gray_image, 1.1, 9) 
#     for(x,y,h,w) in faces:
#         cv2.rectangle(image, (x, y), (x+w, y+h), GREEN, 2)
#         face_width = w
#         centerX = x+w/2
#         centerY = y+h/2

        
#     return face_width,centerX,centerY

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
                i+=1
                cv2.rectangle(img, (int(box.xyxy[0][0]), int(box.xyxy[0][1])),
                            (int(box.xyxy[0][2]), int(box.xyxy[0][3])), BLUE, 2)
                cv2.putText(img, f"{result.names[int(box.cls[0])]}",
                            (int(box.xyxy[0][0]), int(box.xyxy[0][1]) - 10),
                            cv2.FONT_HERSHEY_PLAIN, 2, BLUE, 2)
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
yaw = -90
pitch = 0
time.sleep(2)
setAngleGimbal(yaw,pitch)
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
no_track = 0
while True:
    rval, frame = cap.read()
    
    # face_width_in_frame,centerX,centerY = face_data(frame)
    # face_width_in_frame = 100
    # if centerX < frameWidth:
    #     pitch-=0.1
    # elif centerX > frameWidth:
    #     pitch+=0.1
    
    # if centerY < frameHeight:
    #     pitch+=0.1
    # elif centerY > frameHeight:
    #     pitch-=0.1
    # setAngleGimbal(yaw,pitch)
    
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
        
        # if centerX < frameWidth:
        #     pitch-=0.1
        # elif centerX > frameWidth:
        #     pitch+=0.1
        
        # if centerY < frameHeight:
        #     pitch+=0.1
        # elif centerY > frameHeight:
        #     pitch-=0.1
        # setAngleGimbal(yaw,pitch)
        
        inp = cv2.waitKey(1)
        if inp == ord("q"): 
            break
        elif inp == ord("w"):
            pitch+=1
            setAngleGimbal(yaw,pitch)
        elif inp == ord("s"):
            pitch-=1
            setAngleGimbal(yaw,pitch)
        elif inp == ord("a"):
            yaw-=1
            setAngleGimbal(yaw,pitch)
        elif inp == ord("d"):
            yaw+=1
            setAngleGimbal(yaw,pitch)
        elif 48 <= inp <= 57:
            track_id = inp - 48
            no_track = 1
        elif inp == ord("x"):
            no_track = 0
    # print(yaw,pitch)
		

# closing the camera 
cap.release() 

# closing the windows that are opened 
cv2.destroyAllWindows() 