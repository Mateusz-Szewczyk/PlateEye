import sqlite3
import streamlit as st


def get_connection():
    return sqlite3.connect('./uploaded-file-data/database.db')


def get_cursor(con):
    return con.cursor()


def add_post(username, content, bounding_box, number_plate, image_path, date):
    con = get_connection()
    cur = get_cursor(con)
    xmin, ymin, xmax, ymax = bounding_box
    try:
        cur.execute(
            f"INSERT INTO posts (username, text, xmin, ymin, xmax, ymax, number_plate, image_path, post_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (username, content, xmin, ymin, xmax, ymax, number_plate, image_path, date))
        con.commit()
        return True
    except sqlite3.IntegrityError:
        st.error("Number plate already exists in the database!")
        return False


def get_last_number_plate_data(number: int = 10):
    con = get_connection()
    cur = get_cursor(con)
    cur.execute(f"SELECT * FROM posts ORDER BY unique_id DESC LIMIT {number}")
    return cur.fetchall()


if __name__ == "__main__":
    pass
