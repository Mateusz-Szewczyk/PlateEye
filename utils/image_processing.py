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
    removed_noise_image = remove_noise(image)
    gray = cv2.cvtColor(removed_noise_image, cv2.COLOR_BGR2GRAY)
    deskewed_image = deskew(gray)
    normalized_image = normalize_image(deskewed_image)
    thresholded_image = thresholding(normalized_image)
    return thresholded_image


def deskew(image):
    angle = determine_skew(image)

    if abs(angle) < 0.5:
        return image

    rotated = rotate(image, angle, resize=True) * 255
    return rotated.astype(np.uint8)


def normalize_image(img):
    norm_img = np.zeros((img.shape[0], img.shape[1]))
    img = cv2.normalize(img, norm_img, 0, 255, cv2.NORM_MINMAX)
    return img.astype(np.uint8)


def remove_noise(image):
    return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 15)


def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
