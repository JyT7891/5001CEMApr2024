from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
from tkinter.ttk import Combobox
from tkinter import messagebox
import subprocess

patient_sign_up = tk.Tk()

# y,x
patient_sign_up.minsize(1000, 790)
patient_sign_up.resizable(False, False)
patient_sign_up.title("Sign Up")

# Load and display an image
image = Image.open('CAD.png')
image = ImageTk.PhotoImage(image)

# Create a label to display the image
image_label = Label(patient_sign_up, image=image)
image_label.place(x=220, y=-180)


def check_sign_up():
    # Get the values from the entry fields
    username = insert_username.get()
    password = insert_password.get()
    email = insert_email.get()
    # if email don't have @ error
    if '@' not in email:
        messagebox.showerror("Email Error", "Please check your email!")
    else:
        # if all correct
        messagebox.showinfo("Success", "Sign up successful!")
        patient_sign_up.withdraw()
        patient_sign_up.after(2000, lambda: subprocess.run(
            ["python", "login_page.py"]))  # Wait for 2000 milliseconds (2 seconds) before running login_page.py


def sign():
    # username, email, password, gender, age, blood type
    global insert_username, insert_password, insert_email
    username = Label(patient_sign_up, text="Name            : ", font=('Arial', 20))
    username.place(x=230, y=190)
    insert_username = Entry(patient_sign_up, width=30, font='Arial 19')
    insert_username.place(x=380, y=190)

    password = Label(patient_sign_up, text="Password      : ", font=('Arial', 20))
    password.place(x=230, y=290)
    insert_password = Entry(patient_sign_up, width=30, font=('Arial', 19))
    insert_password.place(x=380, y=290)

    email = Label(patient_sign_up, text="Email             : ", font=('Arial', 20))
    email.place(x=230, y=390)
    insert_email = Entry(patient_sign_up, width=30, font=('Arial', 19))
    insert_email.place(x=380, y=390)

    gender = Label(patient_sign_up, text="Gender          : ", font=('Arial', 20))
    gender.place(x=230, y=490)
    gender_types = ["Male", "Female"]
    gender_type_combobox = Combobox(patient_sign_up, values=gender_types, font=('Arial', 19), state='readonly')
    gender_type_combobox.place(x=380, y=490)

    blood_type = Label(patient_sign_up, text="Blood Type    : ", font=('Arial', 20))
    blood_type.place(x=230, y=590)
    blood_types = ["A", "B", "AB", "O"]
    blood_type_var = StringVar()
    for i, blood_type_option in enumerate(blood_types):
        blood_type_radio = Radiobutton(patient_sign_up, text=blood_type_option, variable=blood_type_var,
                                       value=blood_type_option, font=('Arial', 19))
        blood_type_radio.place(x=380 + i * 100, y=590)

    submit = Button(patient_sign_up, text="Sign Up", height=2, width=30, font=('Arial', 20), command=check_sign_up)
    submit.place(x=250, y=690)
    patient_sign_up.bind("<Return>", check_sign_up)


sign()
patient_sign_up.mainloop()
