import os
import cv2
import numpy as np
from skimage.transform import rotate
from deskew import determine_skew


def prepare_images(uploaded_file, image_dir):
    """
    Prepares the uploaded image for processing.

    Args:
        uploaded_file: The uploaded file object containing the image.
        image_dir: Directory path where the uploaded image is stored.

    Returns:
        Tuple containing two numpy arrays:
            - image_copy: A copy of the uploaded image.
            - image: The uploaded image in RGB format.
    """
    image_path = os.path.join(image_dir, uploaded_file.name)
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Failed to load image at path: {image_path}")
    # Convert image to RGB format
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_copy = image.copy()
    return image_copy, image


def preprocess_image_for_ocr(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Deskew the image
    deskewed_image = deskew(image)
    return deskewed_image


def deskew(image):
    angle = determine_skew(image)
    height, width = image.shape[:2]
    centerX, centerY = (width // 2, height // 2)
    M = cv2.getRotationMatrix2D((centerX, centerY), angle*0.8, 1.0)
    rotated = cv2.warpAffine(image, M, (width, height))
    return rotated.astype(np.uint8)
