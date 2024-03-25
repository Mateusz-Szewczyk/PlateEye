from ultralytics import YOLO
from easyocr import Reader
import time
import torch
import cv2
import os
import csv


CONFIDENCE_THRESHOLD = 0.5
COLOR = (0, 255, 0)

from ultralytics import YOLO
from easyocr import Reader
import time
import torch
import cv2
import os
import csv


CONFIDENCE_THRESHOLD = 0.4
COLOR = (0, 255, 0)

def detect_number_plates(image, model, display=False):
    start = time.time()
    # pass the image through the model and get the detections
    detections = model.predict(image)[0].boxes.data

    # check to see if the detections tensor is not empty
    if detections.shape != torch.Size([0, 6]):

        # initialize the list of bounding boxes and confidences
        boxes = []
        confidences = []

        # loop over the detections
        for detection in detections:
            # extract the confidence (i.e., probability) associated
            # with the prediction
            confidence = detection[4]

            # filter out weak detections by ensuring the confidence
            # is greater than the minimum confidence
            if float(confidence) < CONFIDENCE_THRESHOLD:
                continue

            # if the confidence is greater than the minimum confidence, add
            # the bounding box and the confidence to their respective lists
            boxes.append(detection[:4])
            confidences.append(detection[4])

        print(f"{len(boxes)} Number plate(s) have been detected.")
        # initialize a list to store the bounding boxes of the
        # number plates and later the text detected from them
        number_plate_list= []

        # loop over the bounding boxes
        for i in range(len(boxes)):
            # extract the bounding box coordinates
            xmin, ymin, xmax, ymax = int(boxes[i][0]), int(boxes[i][1]),\
                                     int(boxes[i][2]), int(boxes[i][3])
            # append the bounding box of the number plate
            number_plate_list.append([[xmin, ymin, xmax, ymax]])

            # draw the bounding box and the label on the image
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), COLOR, 2)
            text = "Number Plate: {:.2f}%".format(confidences[i] * 100)
            cv2.putText(image, text, (xmin, ymin - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR, 2)

            if display:
                # crop the detected number plate region
                number_plate = image[ymin:ymax, xmin:xmax]
                # display the number plate
                cv2.imshow(f"Number plate {i}", number_plate)

        end = time.time()
        # show the time it took to detect the number plates
        print(f"Time to detect the number plates: {(end - start) * 1000:.0f} milliseconds")
        # return the list containing the bounding
        # boxes of the number plates
        return number_plate_list
    # if there are no detections, show a custom message
    else:
        print("No number plates have been detected.")
        return []


def recognize_number_plate(image_or_path, reader, number_plate_list, write_to_csv=False):
    start = time.time()
    image = cv2.imread(image_or_path) if isinstance(image_or_path, str) else image_or_path
    for i, box in enumerate(number_plate_list):
        xmin, ymin, xmax, ymax = box[0]
        number_plate = image[ymin:ymax, xmin:xmax]
        # read the text from the number plate
        text = reader.readtext(number_plate, paragraph=True)
        if len(text) == 0:
            text = ["No text detected"]
        else:
            text = str(text[0][1])

        number_plate_list[i].append(text)
        print(number_plate_list[i])
        # draw the text on the image
        cv2.putText(image, text[0], (xmin, ymin - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR, 2)
        if write_to_csv:
            with open("number_plates.csv", "a") as file:
                writer = csv.writer(file)
                writer.writerow([text[0], xmin, ymin, xmax, ymax])



if __name__ == '__main__':
    model = YOLO("../runs/detect/train/weights/best.pt")
    reader = Reader(["en"])
    file_path = "datasets/car-number-plate/images/frame50.jpeg"

    _, file_extension = os.path.splitext(file_path)
    if file_extension in [".jpg", ".jpeg", ".png"]:
        image = cv2.imread(file_path)
        number_plate_list = detect_number_plates(image, model, display=True)
        recognize_number_plate(file_path, reader, number_plate_list, write_to_csv=True)
        cv2.imshow("Image", image)
        cv2.waitKey(0)
    elif file_extension in [".mp4", ".avi", ".wmv", ".flv", ".mkv"]:
        # Add video processing logic here
        video_capture = cv2.VideoCapture(file_path)

        frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(video_capture.get(cv2.CAP_PROP_FPS))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter("output.mp4", fourcc, fps, (frame_width, frame_height))
        while True:
            start = time.time()
            success, frame = video_capture.read()

            if not success:
                print("End of video")
                break

            number_plate_list = detect_number_plates(frame, model)
            end = time.time()
            fps = f"FPS: {1 / (end - start):.2f}"
            cv2.putText(frame, fps, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, COLOR, 8)
            cv2.imshow("Output", frame)
            writer.write(frame)

            if cv2.waitKey(10) == ord("q"):
                break

        video_capture.release()
        writer.release()
        cv2.destroyAllWindows()

