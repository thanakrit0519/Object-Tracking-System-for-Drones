# install opencv "pip install opencv-python" 
import math as Math
import cv2 

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


Known_distance = 50

Known_width = 14.28 #cm

# Colors 
GREEN = (0, 255, 0) 
RED = (0, 0, 255) 
WHITE = (255, 255, 255) 
BLACK = (0, 0, 0) 

# defining the fonts 
fonts = cv2.FONT_HERSHEY_COMPLEX 

# face detector object 
#face_detector = cv2.CascadeClassifier("Haarcascade_frontalface_default.xml") 
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# focal length finder function 
def Focal_Length_Finder(measured_distance, real_width, width_in_rf_image): 

	# finding the focal length 
	focal_length = (width_in_rf_image * measured_distance) / real_width 
	return focal_length 

# distance estimation function 
def Distance_finder(drone_altitude, camera_angle): 

	distance = Math.tan(camera_angle / 180 * Math.pi) * drone_altitude
	# return the distance 
	return distance 

def face_data(image):
    face_width = 0 # making face width to zero
    center_face_x,center_face_y=0,0
    
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray_image, 1.1, 9) 
    for(x,y,h,w) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), GREEN, 2)
        center_face_x = x+w/2
        center_face_y = y+h/2

    # return the face width in pixel
    return center_face_x,center_face_y


# reading reference_image from directory 
# ref_image = cv2.imread("Ref_image.jpg") 

# # find the face width(pixels) in the reference_image 
# ref_image_face_width = face_data(ref_image) 

# Focal_length_found = Focal_Length_Finder( 
# 	Known_distance, Known_width, ref_image_face_width) 

# print(Focal_length_found) 

# # show the reference image 
# cv2.imshow("ref_image", ref_image)

cap = cv2.VideoCapture("rtsp://192.168.144.25:8554/video1") 

clat,clon = 13.75,100.5
bearing = 70
drone_altitude = 100
camera_angle = 60
# looping through frame, incoming from 
# camera/video 
while True:
    _, frame = cap.read()
    
    center_face_x,center_face_y = face_data(frame)
        
    Distance = Distance_finder(drone_altitude,camera_angle)
        
    lat, lon = destinationPoint(clat, clon, Distance, bearing)
        
        # draw line as background of text
    cv2.line(frame, (30, 30), (230, 30), RED, 32) 
    cv2.line(frame, (30, 30), (230, 30), BLACK, 28)
        
        # Drawing Text on the screen
    cv2.putText( frame, f"Distance: {round(Distance,2)} M", (30, 35), fonts, 0.6, GREEN, 2)
    cv2.putText( frame, f"Camera lat: {round(clat,6)} Camera lon: {round(clon,6)}", (30, 65), fonts, 0.6, GREEN, 1)
    cv2.putText( frame, f"Object lat: {round(lat,6)} Object lon: {round(lon,6)}", (30, 85), fonts, 0.6, GREEN, 1)
        
        # show the frame on the screen 
    cv2.imshow("frame", frame) 
        
        # quit the program if you press 'q' on keyboard
    if cv2.waitKey(1) == ord("q"): 
        break
    
    while not (680 >= center_face_x >= 600 and 400 >= center_face_y >= 320):
        if  not (680 >= center_face_x >= 600):
            if cv2.waitKey(1) == ord("a"):
                center_face_x = 640
        elif not (400 >= center_face_y >= 320):
            if cv2.waitKey(1) == ord("a"):
                center_face_y = 360
		

# closing the camera 
cap.release() 

# closing the windows that are opened 
cv2.destroyAllWindows() 