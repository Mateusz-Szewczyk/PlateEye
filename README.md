# PlateEye - Number Plate Detection and Recognition :car:
https://plateeye.streamlit.app/

PlateEye is a Streamlit web application that allows users to upload images containing vehicle number plates for detection and recognition. The application provides a user-friendly interface for performing these tasks and adding comments to the recognized number plates.

## Features
- Number Plate Detection: Utilizes computer vision techniques to detect number plates within uploaded images. (with YOLOv8 finetuned by me)
- Number Plate Recognition: Recognizes characters on the detected number plates using optical character recognition (OCR) methods.
- Posting System: Enables users to add posts to the recognized number plates for further context or annotation.
- User Authentication: Requires user authentication for accessing the application's features, ensuring privacy and security.
- Responsive UI: Built with Streamlit, providing an intuitive and interactive user interface that adapts to various screen sizes.

## Usage
1. Upload an image containing a vehicle number plate using the file uploader.
1. PlateEye will detect and highlight the number plate(s) in the uploaded image.
1. If number plates are detected, the application will recognize the characters on the plates.
1. You can add comments to the recognized number plates for additional information or context.
1. After adding comments, click the "Post" button to save the data.

### License
PlateEye is licensed under the MIT License.

#### Acknowledgements
This project utilizes various open-source libraries and tools, including Streamlit, OpenCV, and easyocr.
Special thanks to Streamlit for providing an excellent platform for building interactive web applications with Python.
