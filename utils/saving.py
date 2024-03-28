import csv
import os


def create_image_dir(uploaded_file, username):
    file_name = uploaded_file.name
    uploaded_file_path = "uploaded-file-data/uploads"
    csv_path = os.path.join(uploaded_file_path, "number_plates.csv")
    image_dir = os.path.join(uploaded_file_path, username)
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    if not os.path.exists(uploaded_file_path):
        os.makedirs(uploaded_file_path)
    with open(os.path.join(image_dir, file_name, ), "wb") as file:
        file.write(uploaded_file.getbuffer())
    return image_dir


def write_to_csv_file(image_or_path, number_plate_list):
    uploaded_file_data = "uploaded-file-data"
    csv_path = os.path.join(uploaded_file_data, "number_plates.csv")

    if not os.path.exists(uploaded_file_data):
        os.makedirs(uploaded_file_data)

    # save the image with the detected number plates

    if not os.path.isfile(csv_path):
        with open(csv_path, "w") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["id", "image", "bbox", "text"])

    with open(csv_path, "a") as csv_file:
        # create a writer object
        csv_writer = csv.writer(csv_file)
        # write the header
        # loop over the `number_plate_list` list
        for i, (box, text) in enumerate(number_plate_list):
            # write the image path, bounding box coordinates,
            # and detected text to the CSV file
            csv_writer.writerow([i, image_or_path, box, text])