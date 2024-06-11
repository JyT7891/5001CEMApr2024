from tkinter import *
import tkinter as tk

import PIL
from PIL import Image, ImageTk
from tkinter.ttk import Combobox
from tkinter import messagebox
import subprocess
from fire_base import getClient, initializeFirebase

patient_sign_up = tk.Tk()

# y,x
patient_sign_up.minsize(1000, 790)
patient_sign_up.resizable(False, False)
patient_sign_up.title("Sign Up")

# Load and display an image
image = PIL.Image.open('CAD.png')
image = PIL.ImageTk.PhotoImage(image)

# Create a label to display the image
image_label = Label(patient_sign_up, image=image)
image_label.place(x=220, y=-180)


def check_sign_up():
    # Import the function from run_script.py
    from run_script import run_script1

    # Get the values from the entry fields
    username = insert_username.get()
    password = insert_password.get()
    email = insert_email.get()
    gender = gender_type_combobox.get()
    blood = blood_type_var.get()
    age = insert_age.get()

    # if email don't have @ error
    if '@' not in email:
        messagebox.showerror("Email Error", "Please check your email!")
    else:
        # if all correct
        conn = initializeFirebase()
        db = getClient()

        docRef = db.collection('user').document(username)
        docRef.set({
            'username': username,
            'age': age,
            'email': email,
            'password': password,
            'gender': gender,
            'bloodType': blood,
        })

        messagebox.showinfo("Success", "Sign up successful!")
        patient_sign_up.destroy()
        # Call the function to run the script
        run_script1('login_page.py')


def sign():
    # name, email, password, gender, age, blood type
    global insert_username, insert_age, insert_email, insert_password, gender_type_combobox, blood_type_var
    name = Label(patient_sign_up, text="Name         :", font=('Arial', 20))
    name.place(x=200, y=180)
    insert_username = Entry(patient_sign_up, width=30, font='Arial 19')
    insert_username.place(x=380, y=180)

    age = Label(patient_sign_up, text="Age            :", font=('Arial', 20))
    age.place(x=200, y=260)
    insert_age = Entry(patient_sign_up, width=30, font=('Arial', 19))
    insert_age.place(x=380, y=260)

    email = Label(patient_sign_up, text="Email          :", font=('Arial', 20))
    email.place(x=200, y=340)
    insert_email = Entry(patient_sign_up, width=30, font=('Arial', 19))
    insert_email.place(x=380, y=340)

    password = Label(patient_sign_up, text="Password    :", font=('Arial', 20))
    password.place(x=200, y=420)
    insert_password = Entry(patient_sign_up, width=30, font=('Arial', 19))
    insert_password.place(x=380, y=420)

    gender = Label(patient_sign_up, text="Gender       :", font=('Arial', 20))
    gender.place(x=200, y=510)
    gender_types = ["Male", "Female"]
    gender_type_combobox = Combobox(patient_sign_up, values=gender_types, font=('Arial', 19), state='readonly')
    gender_type_combobox.place(x=380, y=510)

    blood_type = Label(patient_sign_up, text="Blood Type  :", font=('Arial', 20))
    blood_type.place(x=200, y=600)
    blood_types = ["A", "B", "AB", "O"]
    blood_type_var = StringVar()
    for i, blood_type_option in enumerate(blood_types):
        blood_type_radio = Radiobutton(patient_sign_up, text=blood_type_option, variable=blood_type_var,
                                       value=blood_type_option, font=('Arial', 19))
        blood_type_radio.place(x=380 + i * 100, y=600)

    submit = Button(patient_sign_up, text="Sign Up", height=2, width=30, font=('Arial', 20), command=check_sign_up)
    submit.place(x=250, y=690)
    patient_sign_up.bind("<Return>", check_sign_up)


sign()
patient_sign_up.mainloop()
