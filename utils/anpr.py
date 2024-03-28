import time
import cv2
import torch
from easyocr import Reader
from ultralytics import YOLO
from utils.image_processing import preprocess_image_for_ocr
from utils.saving import write_to_csv_file

CONFIDENCE_THRESHOLD = 0.4
COLOR = (0, 255, 0)


def model_and_reader():
    model = YOLO("runs/detect/train/weights/best.pt")
    reader = Reader(["en"], gpu=True)
    return model, reader


def detect_number_plates(image, model, display=False):
    """
    Detects number plates in the input image using the provided model.

    Args:
        image: Input image (numpy array or path).
        model: YOLO model for plate detection.
        display: Whether to display the detected plates (default is False).

    Returns:
        List of bounding boxes for the detected number plates, each box represented as [xmin, ymin, xmax, ymax].
        If no number plates are detected, returns an empty list.
    """
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
        bounding_boxes_list = []

        # loop over the bounding boxes
        for i in range(len(boxes)):
            # extract the bounding box coordinates
            xmin, ymin, xmax, ymax = int(boxes[i][0]), int(boxes[i][1]), \
                int(boxes[i][2]), int(boxes[i][3])
            # append the bounding box of the number plate
            bounding_boxes_list.append([[xmin, ymin, xmax, ymax]])

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
        return bounding_boxes_list
    # if there are no detections, show a custom message
    else:
        print("No number plates have been detected.")
        return []


def recognize_number_plates(image_or_path,
                            reader,
                            number_plate_list,
                            write_to_csv=True):
    """
    Recognizes the text from the detected number plates and optionally writes the results to a CSV file.

    Parameters:
    - image_or_path (str or numpy.ndarray): Either the path to the image file or the image itself.
    - reader (easyocr.Reader): An instance of the EasyOCR reader.
    - number_plate_list (list): A list containing the bounding boxes of the detected number plates.
    - write_to_csv (bool): Whether to write the results to a CSV file (default is True).

    Returns:
    - list: The updated number_plate_list with the detected text appended to each entry.

    """
    start = time.time()
    image_or_path = str(image_or_path)
    # if the image is a path, load the image; otherwise, use the image
    image = cv2.imread(image_or_path, cv2.IMREAD_COLOR) if isinstance(image_or_path, str) else image_or_path
    print(f"anpr, image dtype: {type(image)}")
    image = preprocess_image_for_ocr(image)
    number_plates_img_list = []
    for i, box in enumerate(number_plate_list):
        # crop the number plate region
        xmin, ymin, xmax, ymax = box[i]

        # Expand the box by 20 pixels in every dimension
        xmin_expanded = max(0, xmin - 20)
        ymin_expanded = max(0, ymin - 20)
        xmax_expanded = min(image.shape[1], xmax + 20)
        ymax_expanded = min(image.shape[0], ymax + 20)

        # Crop the number plate region using the expanded box
        np_image = image[ymin_expanded:ymax_expanded, xmin_expanded:xmax_expanded]
        number_plates_img_list.append(np_image)
        # detect the text from the license plate using the EasyOCR reader
        detection = reader.readtext(np_image, paragraph=True)

        if len(detection) == 0:
            # if no text is detected, set the `text` variable to an empty string
            text = ""
        else:
            # set the `text` variable to the detected text
            text = str(detection[0][1])
        # update the `number_plate_list` list, adding the detected text
        text = process_text(text)
        number_plate_list[i].append(text)

    if write_to_csv:
       write_to_csv_file(image_or_path, number_plate_list)

    return number_plate_list, number_plates_img_list


def process_text(text: str) -> str:
    remove_chars = ["@", "'", '"', ":", ";", "!", "?", ".", ",", " ", "|", "*", "#", "$", "%", "&", "(", ")", "[", "]", "{", "}", "<", ">", "+", "-", "_", "=", "/"]
    for char in remove_chars:
        text = text.replace(char, "")
    return text