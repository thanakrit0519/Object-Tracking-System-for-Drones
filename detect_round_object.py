import cv2 
import numpy as np 
from controlGimbal import setAngleGimbal
from calLatLong002 import cal_objectGPS1
import time
  
# img = cv2.imread('eyes.jpg', cv2.IMREAD_COLOR) 

yaw = -90
pitch = 0
# time.sleep(2)
# setAngleGimbal(yaw,pitch)
# time.sleep(4)
cap = cv2.VideoCapture('rtsp://192.168.144.25:8554/video1')

# cap = cv2.VideoCapture(0)

frameWidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
frameHeight = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(frameWidth,frameHeight)
track_id = -1
on_track = 0

while True:
    rval, img = cap.read()
  
    # Convert to grayscale. 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    
    # Blur using 3 * 3 kernel. 
    gray_blurred = cv2.blur(gray, (3, 3)) 
    
    # Apply Hough transform on the blurred image. 
    detected_circles = cv2.HoughCircles(gray_blurred,  
                    cv2.HOUGH_GRADIENT, 1, 20, param1 = 50, 
                param2 = 30, minRadius = 1, maxRadius = 40) 
    
    # Draw circles that are detected. 
    if detected_circles is not None: 
    
        # Convert the circle parameters a, b and r to integers. 
        detected_circles = np.uint16(np.around(detected_circles)) 
    
        for pt in detected_circles[0, :]: 
            a, b, r = pt[0], pt[1], pt[2] 
    
            # Draw the circumference of the circle. 
            cv2.circle(img, (a, b), r, (0, 255, 0), 2) 
    
            # Draw a small circle (of radius 1) to show the center. 
            cv2.circle(img, (a, b), 1, (0, 0, 255), 3) 
            
            if on_track == 1:
                if a < frameWidth/2 - 20:
                    yaw+=0.2
                elif a > frameWidth/2 + 20:
                    yaw-=0.2
                if b < frameHeight/2 - 20:
                    pitch+=0.2
                elif b > frameHeight/2 + 20:
                    pitch-=0.2
                if yaw > 180 :
                    yaw = -180 + 0.2
                elif yaw < -180:
                    yaw = 180 - 0.2
                setAngleGimbal(yaw,pitch)
            
    cv2.imshow("Detected Circle", img) 
        
        
        
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
        on_track = 1
    elif inp == ord("x"):
        on_track = 0
            # cv2.waitKey(0) 
cap.release() 

# closing the windows that are opened 
cv2.destroyAllWindows() 