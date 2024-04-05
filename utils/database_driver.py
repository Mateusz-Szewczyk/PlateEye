import sqlite3
import os
import streamlit as st

def get_connection():
    return sqlite3.connect("number_plate_database.db")

def get_cursor(con):
    return con.cursor()

def create_database():
    # Check if the database file exists
    if not os.path.exists("number_plate_database.db"):
        # If the database file does not exist, create a new one and establish a connection
        conn = sqlite3.connect("number_plate_database.db")
        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()
        # Create the 'posts' table
        cursor.execute("""
            CREATE TABLE posts (
                username TEXT,
                unique_id INTEGER PRIMARY KEY AUTOINCREMENT,
                number_plate TEXT,
                xmin INTEGER,
                ymin INTEGER,
                xmax INTEGER,
                ymax INTEGER,
                text TEXT,
                image_path TEXT,
                post_date DATE
            )
        """)
        # Commit the changes and close the connection
        conn.commit()
        conn.close()
        print("Database and 'posts' table created successfully.")
        return conn, cursor
    else:
        return get_connection(), get_cursor(get_connection())
        print("Database file already exists.")


def add_post(username, content, bounding_box, number_plate, image_path, date):
    con, cur = create_database()
    xmin, ymin, xmax, ymax = bounding_box
    try:
        cur.execute(
            f"INSERT INTO posts (username, text, xmin, ymin, xmax, ymax, number_plate, image_path, post_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (username, content, xmin, ymin, xmax, ymax, number_plate, image_path, date))
    except sqlite3.IntegrityError:
        st.error("Number plate already exists in the database!")
    con.commit()


def get_last_number_plate_data(number: int = 10):
    con = get_connection()
    cur = get_cursor(con)
    cur.execute(f"SELECT * FROM posts ORDER BY unique_id DESC LIMIT {number}")
    return cur.fetchall()


if __name__ == "__main__":
    pass
