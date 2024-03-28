import sqlite3
import streamlit as st

con = sqlite3.connect('./uploaded-file-data/database.db')
cur = con.cursor()

def add_post(username, content, bounding_box, number_plate, image_path,):
    xmin, ymin, xmax, ymax = bounding_box
    try:
        cur.execute(f"INSERT INTO number_plates (username, content, xmin, ymin, xmax, ymax, number_plate, image_path) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (username, content, xmin, ymin, xmax, ymax, number_plate, image_path))
    except sqlite3.IntegrityError:
        st.subheader("Number plate already exists in the database!")
    con.commit()


def get_last_number_plate_data(number: int = 10):
    cur.execute(f"SELECT * FROM number_plates ORDER BY unique_id DESC LIMIT {number}")
    return cur.fetchall()

if __name__ == "__main__":
    pass
