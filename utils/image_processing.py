import os
import cv2
import numpy as np
from skimage.transform import rotate
from deskew import determine_skew


def prepare_images(image_path):
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
    # Load the image
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError(f"Failed to load image at path: {image_path}")
    # Convert image to RGB format
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_copy = image.copy()
    return image_copy, image


def preprocess_image_for_ocr(image):
    removed_noise_image = remove_noise(image)
    contrast = increase_contrast(removed_noise_image)
    gray = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)
    thresholded_image = thresholding(gray)
    # TODO - Implement deskewing
    # deskewed_image = deskew(thresholded_image)
    return thresholded_image


def increase_contrast(img):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l_channel, a, b = cv2.split(lab)

    # Applying CLAHE to L-channel
    # feel free to try different values for the limit and grid size:
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl = clahe.apply(l_channel)

    # merge the CLAHE enhanced L-channel with the a and b channel
    limg = cv2.merge((cl, a, b))

    # Converting image from LAB Color model to BGR color space
    enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    # Stacking the original image with the enhanced image
    result = np.hstack((img, enhanced_img))
    return result


def remove_noise(image):
    # Apply denoising
    return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 15)


def thresholding(image):
    return cv2.threshold(image, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
