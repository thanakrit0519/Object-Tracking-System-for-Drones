import cv2 
import numpy as np 
from controlGimbal import setAngleGimbal, Zoom
from calLatLong002 import cal_objectGPS1
import time
import math
  
# img = cv2.imread('eyes.jpg', cv2.IMREAD_COLOR) 


yaw = -90
pitch = 0

on_track = 0

moveTime=0
x=1

image = cv2.imread("/home/song/CoopProject/img/P_20241105_230113.jpg")
img = cv2.resize(image, (1477, 1108))
img2 = cv2.imread("/home/song/CoopProject/img/White_background.png")
img2 = cv2.resize(img2, (1000, 1000))
    # time.sleep(1)
    # Convert to grayscale. 

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 

# Blur using 3 * 3 kernel. 
gray_blurred = cv2.blur(gray, (3, 3)) 

# Apply Hough transform on the blurred image. 
detected_circles = cv2.HoughCircles(gray_blurred,  
                cv2.HOUGH_GRADIENT, 1, 20, param1 = 70, 
            param2 = 30, minRadius = 1, maxRadius = 200) 
GREEN = (0, 255, 0) 
RED = (0, 0, 255) 
WHITE = (255, 255, 255) 
BLACK = (0, 0, 0) 
BLUE = (255, 0, 0) 
output = []
# Draw circles that are detected. 
# cv2.circle(img2, (120, 84), 5, (0, 255, 0), 2) 
# cv2.circle(img2, (117, 168), 5, (0, 255, 0), 2) 
# cv2.circle(img2, (120, 254), 5, (0, 255, 0), 2) 
while True:
    if detected_circles is not None: 

        # Convert the circle parameters a, b and r to integers. 
        detected_circles = np.uint16(np.around(detected_circles)) 
        i = 0
        for pt in detected_circles[0, :]: 
            a, b, r = pt[0], pt[1], pt[2] 
            output.append([round((r*2)*250/146),a,b])
            # Draw the circumference of the circle. 
            cv2.circle(img, (a, b), r, (0, 255, 0), 2) 

            # Draw a small circle (of radius 1) to show the center. 
            cv2.circle(img, (a, b), 1, (0, 0, 255), 3) 
            
            cv2.putText(img, f"id : {i}",(a-r, b-r - 10),cv2.FONT_HERSHEY_PLAIN, 2, BLUE, 2)
            
            x= 1000 - round((1753.8*(5/round((r*2)*250/146))+7.3749)*math.cos(0.46))*10
            cv2.circle(img2, (round(a/1108*1000), x), 50, (0, 255, 0), 2) 
            cv2.putText(img2, f"id : {i}", (round(a/1108*1000)-40, x-55),cv2.FONT_HERSHEY_PLAIN, 2, BLUE, 2)
            
            i=i+1
            # print(time.time())
                
    # cv2.circle(img, (int(frameWidth)//2,int(frameHeight)//2), 4, (255, 0, 0), 2)      
    print(output)  
    cv2.imshow("Detected Circle", img) 
    cv2.imshow("Detected Circle2", img2) 
        
        
        
    inp = cv2.waitKey(0)
    if inp == ord('q'):
        break
    # cv2.waitKey(0) 

# closing the windows that are opened 
cv2.destroyAllWindows() 