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
    thresholded_image = thresholding(gray)
    # TODO - Implement deskewing
    # deskewed_image = deskew(thresholded_image)
    return thresholded_image

# def deskew(image):
#     coords = np.column_stack(np.where(image > 0))
#     angle = cv2.minAreaRect(coords)[-1]
#
#     # Additional angle adjustment based on image content
#     if angle < -45:
#         angle = -(90 + angle)
#     else:
#         angle = -angle
#
#     # Visualize the angle to debug
#     print("Rotation angle:", angle)
#
#     (h, w) = image.shape[:2]
#     center = (w // 2, h // 2)
#     M = cv2.getRotationMatrix2D(center, angle, 1.0)
#     rotated = cv2.warpAffine(image, M, (w, h),
#                              flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
#     return rotated

def remove_noise(image):
    return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 15)

def thresholding(image):
    return cv2.threshold(image, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]