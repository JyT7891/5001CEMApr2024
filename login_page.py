import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from fire_base import getClient, initializeFirebase
from run_script import run_script1
import os

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

def email_exists_in_firestore(username):
    try:
        user_doc = db.collection('user').document(username).get()
        return user_doc.exists
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def password_matches(username, password):
    try:
        doc = db.collection('user').document(username).get()
        if doc.exists:
            user_data = doc.to_dict()
            if user_data.get('password') == password:
                return user_data.get('userType'), username
        return None, None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

def check_login(event=None):
    username = insert_username.get()
    password = insert_password.get()

    if email_exists_in_firestore(username):
        user_type, user_id = password_matches(username, password)
        if user_type and user_id:
            os.environ["USERNAME"] = user_id  # Set the username as an environment variable
            messagebox.showinfo("Login Successful", "Login successful!")
            patient_login.destroy()
            if user_type == "user":
                run_script1('user_home_page.py')
            elif user_type == "admin":
                run_script1('clinic_web.py')
            else:
                messagebox.showerror("Login Failed", "User type is not recognized.")
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")
    else:
        messagebox.showerror("Login Failed", "Email does not exist. Please sign up.")

def check_sign_up():
    patient_login.destroy()
    run_script1('sign_up.py')

def login_page():
    global insert_username, insert_password

    tk.Label(patient_login, text="Username   : ", font=('Arial', 20)).place(x=200, y=310)
    insert_username = tk.Entry(patient_login, width=30, font='Arial 19')
    insert_username.place(x=380, y=310)

    tk.Label(patient_login, text="Password    : ", font=('Arial', 20)).place(x=200, y=410)
    insert_password = tk.Entry(patient_login, width=30, show="*", font='Arial 19')
    insert_password.place(x=380, y=410)

    tk.Button(patient_login, text="Sign Up", height=2, width=15, font=('Arial', 20), command=check_sign_up).place(x=230, y=510)
    tk.Button(patient_login, text="Login", height=2, width=15, font=('Arial', 20), command=check_login).place(x=500, y=510)

    patient_login.bind("<Return>", check_login)

def main():
    login_page()
    patient_login.mainloop()

if __name__ == '__main__':
    main()
