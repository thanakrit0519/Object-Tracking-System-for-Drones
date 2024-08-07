
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
GREEN = (0, 255, 0) 
model = YOLO("/home/song/CoopProject/trained_model_visdrone2019_1_7_2024/yolov8x-p6.pt")
def predict(chosen_model, img, classes=[], conf=0.5):
    if classes:
        results = chosen_model.predict(img, classes=classes, conf=conf)
    else:
        results = chosen_model.predict(img, conf=conf)

    return results

def predict_and_detect(chosen_model, img, classes=[], conf=0.5):
    results = predict(chosen_model, img, classes, conf=conf)

    for result in results:
        for box in result.boxes:
            cv2.rectangle(img, (int(box.xyxy[0][0]), int(box.xyxy[0][1])),
                          (int(box.xyxy[0][2]), int(box.xyxy[0][3])), (255, 0, 0), 2)
            cv2.putText(img, f"{result.names[int(box.cls[0])]}",
                        (int(box.xyxy[0][0]), int(box.xyxy[0][1]) - 10),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
    return img, results
cap = cv2.VideoCapture(0)
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

    

