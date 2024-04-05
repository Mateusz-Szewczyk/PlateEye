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
        try:
            cursor.execute('CREATE TABLE posts (username varchar(255), unique_id INTEGER PRIMARY KEY, number_plate varchar(255), xmin INTEGER, ymin INTEGER, xmax INTEGER, ymax INTEGER, `text` varchar(255), image_path varchar(255), post_date DATE)')

        except Exception as e:
            print(e)
        # Commit the changes and close the connection
        conn.commit()
        conn.close()
        print("Database and 'posts' table created successfully.")
        return conn, cursor  # Return the connection and cursor
    else:
        conn = get_connection()  # Get the connection
        cur = get_cursor(conn)   # Get the cursor
        return conn, cur         # Return the connection and cursor


def add_post(username, content, bounding_box, number_plate, image_path, date):
    con, cur = create_database()
    xmin, ymin, xmax, ymax = bounding_box
    try:
        cur.execute(
            f"INSERT INTO posts (username, text, xmin, ymin, xmax, ymax, number_plate, image_path, post_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (username, content, xmin, ymin, xmax, ymax, number_plate, image_path, date))
        con.commit()
        con.close()
        return True
    except sqlite3.IntegrityError:
        st.error("Number plate already exists in the database!")
        return False


def get_last_number_plate_data(number: int = 10):
    con = get_connection()
    cur = get_cursor(con)

    # Sprawdź, czy tabela "posts" istnieje
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='posts'")
    table_exists = cur.fetchone()

    if not table_exists:
        # Jeśli tabela nie istnieje, utwórz ją
        cur.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                username varchar(255),
                unique_id INTEGER PRIMARY KEY,
                number_plate varchar(255),
                xmin INTEGER,
                ymin INTEGER,
                xmax INTEGER,
                ymax INTEGER,
                `text` varchar(255),
                image_path varchar(255),
                post_date DATE
            )
        ''')
        con.commit()

    # Wykonaj zapytanie SELECT
    cur.execute(f"SELECT * FROM posts ORDER BY unique_id DESC LIMIT {number}")
    return cur.fetchall()


if __name__ == "__main__":
    create_database()
    print(get_last_number_plate_data())
