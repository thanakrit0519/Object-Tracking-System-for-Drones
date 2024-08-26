
import cv2
from ultralytics import YOLO

object_class = [
  'pedestrian',
  'people',
  'bicycle',
  'car',
  'van',
  'truck',
  'tricycle',
  'awning-tricycle',
  'bus',
  'motor']
BLUE = (255, 0, 0) 
model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture('rtsp://192.168.144.25:8554/video1')
w=cap.get(cv2.CAP_PROP_FRAME_WIDTH)
h=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(w,h)
def predict(chosen_model, img, conf=0.1):
    results = chosen_model(source=img,stream=True)
    return results

def predict_and_detect(chosen_model, img, conf=0.5):
    results = predict(chosen_model, img, conf=conf)

    for result in results:
        for box in result.boxes:
            cv2.rectangle(img, (int(box.xyxy[0][0]), int(box.xyxy[0][1])),
                          (int(box.xyxy[0][2]), int(box.xyxy[0][3])), BLUE, 2)
            cv2.putText(img, f"{result.names[int(box.cls[0])]}",
                        (int(box.xyxy[0][0]), int(box.xyxy[0][1]) - 10),
                        cv2.FONT_HERSHEY_PLAIN, 2, BLUE, 2)
    return img, results

while True:
    ret, image = cap.read()

    if ret == True:
        img,results = predict_and_detect(model,image)
        cv2.imshow('video output', img)
        k = cv2.waitKey(1)
        if k == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()

    

