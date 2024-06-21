from tkinter import *
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from fire_base import getClient, initializeFirebase
# Import the function from run_script.py
from run_script import run_script1

# Initialize the Firebase Admin SDK
conn = initializeFirebase()
db = getClient()

# Create the main Tkinter window
patient_login = tk.Tk()
patient_login.minsize(1000, 790)
patient_login.resizable(False, False)
patient_login.title("Login")

# Load and display an image
image = Image.open('CAD.png')
image = ImageTk.PhotoImage(image)
image_label = tk.Label(patient_login, image=image)
image_label.place(x=220, y=-180)


def email_exists_in_firestore(username1):
    try:
        # search in user database
        doc_ref = db.collection('user').document(username1)
        doc = doc_ref.get()
        # search in doctor database
        doc1_ref = db.collection('user').document(username1)
        doc1 = doc1_ref.get()
        return doc.exists, doc1.exists
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def password_matches(username1, password):
    try:
        doc_ref = db.collection('user').document(username1)
        doc = doc_ref.get()
        if doc.exists:
            user_data = doc.to_dict()
            if user_data.get('password') == password:
                return "user", username1
        # Check if user exists in 'doctor' collection
        doc_ref = db.collection('doctor').document(username1)
        doc = doc_ref.get()
        if doc.exists:
            user_data = doc.to_dict()
            if user_data.get('password') == password:
                return "doctor", username1
        return None, None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None


def check_login(event=None):
    username1 = insert_username.get()
    password = insert_password.get()

    if email_exists_in_firestore(username1):
        user_type, user_id = password_matches(username1, password)
        if user_type and user_id:
            if user_type == "user":
                messagebox.showinfo("Login Successful", "Login successful!")
                patient_login.destroy()
                run_script1('user_home_page.py', user_id)
            elif user_type == "doctor":
                messagebox.showinfo("Login Successful", "Login successful!")
                patient_login.destroy()
                run_script1('doctor_web.py', user_id)
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")
    else:
        messagebox.showerror("Login Failed", "Email does not exist. Please sign up.")


def check_sign_up():
    patient_login.destroy()
    run_script1('sign_up.py')


# Function to set up the login page
def login_page():
    global insert_username, insert_password
    username = Label(patient_login, text="Username   : ", font=('Arial', 20))
    username.place(x=200, y=310)
    insert_username = Entry(patient_login, width=30, font='Arial 19')
    insert_username.place(x=380, y=310)

    password = Label(patient_login, text="Password    : ", font=('Arial', 20))
    password.place(x=200, y=410)
    insert_password = Entry(patient_login, width=30, show="*", font=('Arial', 19))
    insert_password.place(x=380, y=410)

    sign_in = Button(patient_login, text="Sign Up", height=2, width=15, font=('Arial', 20),
                     command=check_sign_up)
    sign_in.place(x=230, y=510)

    submit = Button(patient_login, text="Login", height=2, width=15, font=('Arial', 20), command=check_login)
    submit.place(x=500, y=510)
    patient_login.bind("<Return>", check_login)


def main():
    # Set up the login page
    login_page()

    # Run the Tkinter main loop
    patient_login.mainloop()


if __name__ == '__main__':
    main()
