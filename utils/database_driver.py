import sqlite3
import streamlit as st

con = sqlite3.connect('./uploaded-file-data/database.db')
cur = con.cursor()


def add_number_plate_data(username, number_plate, bounding_box):
    xmin, ymin, xmax, ymax = bounding_box
    try:
        cur.execute("INSERT INTO number_plates (username, number_plate, xmin, ymin, xmax, ymax) VALUES (?, ?, ?, ?, ?, ?)", (username, number_plate, xmin, ymin, xmax, ymax))
    except sqlite3.IntegrityError:
        st.subheader("Number plate already exists in the database!")
    con.commit()



if __name__ == "__main__":
    add_number_plate_data("testing", "", (100, 200, 300, 400))

