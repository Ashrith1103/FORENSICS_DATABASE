import streamlit as st
from add import add
from read import read
from read1 import read1
from queries import predef_queries, query_cmd
from update import update
from delete import delete
import base64
import base64
import streamlit as st


def set_background(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    
    # Encode the image data in base64
    encoded_image = base64.b64encode(data).decode('utf-8')  # Fix: use base64.b64encode and decode to string
    
    # Use the encoded image in your app
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_image}");
            background-size: cover;
            background-attachment: fixed;
            color: #ffffff;  /* Change text color for better visibility */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Example usage
#set_background("C:/Users/HP/Desktop/Forensics-DBMS/Python/image.png")



# Define user credentials and roles


def main():
    st.title("Forensics Database")

    # Login page
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login()
    else:
        st.sidebar.title("Navigation")
        role_based_menu()

import pymysql

def get_db_connection():
    try:
        mydb = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="forensics",
            cursorclass=pymysql.cursors.DictCursor  # Ensures query results as dictionaries
        )
        return mydb
    except pymysql.MySQLError as e:
        print(f"Error connecting to the database: {e}")
        return None

def close_db_connection(mydb):
    if mydb:
        mydb.close()


# Login function
def login():
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        mydb = get_db_connection()  # Make sure get_db_connection() returns a valid connection
        if mydb:
            try:
                with mydb.cursor() as curs:
                    query = "SELECT * FROM user_credentials WHERE Username = %s AND Password = %s"
                    curs.execute(query, (username, password))
                    user = curs.fetchone()

                    if user:
                        st.success(f"Welcome {username}")
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.role = user["Role"]
                    else:
                        st.error("Invalid username or password")
            finally:
                close_db_connection(mydb)  # Properly close the connection
        else:
            st.error("Could not connect to the database.")

# Logout function
def logout():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    st.success("Logged out successfully")
    
    # Role-Based Menu
def role_based_menu():
    if st.session_state.role == "admin":
        menu = ["Add Records", "View Tables","Update Record", "Delete Records", "Run Predefined Queries", "CMD", "Logout"]
    else:
        menu = ["View Tables", "Run Predefined Queries", "CMD", "Logout"]

    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Records" and st.session_state.role == "admin":
        add()
    elif choice == "View Tables" and st.session_state.role == "admin":
        read()
    elif choice == "View Tables" and st.session_state.role == "user":
        read1()
    elif choice == "Update Record" and st.session_state.role == "admin":
        update()
    elif choice == "Delete Records" and st.session_state.role == "admin":
        delete()
    elif choice == "Run Predefined Queries":
        predef_queries()
    elif choice == "CMD":
        query_cmd()
    elif choice == "Logout":
        logout()

if __name__ == '__main__':
    main()