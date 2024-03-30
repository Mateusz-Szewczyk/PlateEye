import csv
import os
from datetime import datetime

def create_image_dir(uploaded_file, username):
    date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    uploaded_file_path = "uploaded-file-data/uploads"
    image_dir = os.path.join(uploaded_file_path, username)
    image_path = os.path.join(image_dir, f'{date}.{uploaded_file.name.split(".")[1]}')
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    with open(os.path.join(image_path), "wb") as f:
        f.write(uploaded_file.getbuffer())
    return image_dir, image_path
