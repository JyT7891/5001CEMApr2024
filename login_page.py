from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import subprocess

patient_login = tk.Tk()

# y,x
patient_login.minsize(1000, 790)
patient_login.resizable(False, False)
patient_login.title("Login")

# Load and display an image
image = Image.open('CAD.png')
image = ImageTk.PhotoImage(image)

image_label = tk.Label(patient_login, image=image)
image_label.place(x=220, y=-180)


def check_login():
    # check username and password
    # username1 = insert_username.get()  # Get the text from the username field
    # print("Username:", username1)
    # password1 = insert_password.get()
    # if correct run into homepage
    patient_login.withdraw()
    subprocess.run(["python", "home_page.py"])

    # else sign up page


def check_sign_up():
    patient_login.withdraw()
    # Close the current Tkinter window
    patient_login.after(2000, lambda: subprocess.run(["python", "sign_up.py"]))


def login_page():
    global insert_username, insert_password
    username = Label(patient_login, text="Email           : ", font=('Arial', 20))
    username.place(x=230, y=310)
    insert_username = Entry(patient_login, width=30, font='Arial 19')
    insert_username.place(x=380, y=310)

    password = Label(patient_login, text="Password    : ", font=('Arial', 20))
    password.place(x=230, y=410)
    insert_password = Entry(patient_login, width=30, show="*", font=('Arial', 19))
    insert_password.place(x=380, y=410)

    sign_in = Button(patient_login, text="Sign Up", height=2, width=15, font=('Arial', 20),
                     command=check_sign_up)
    sign_in.place(x=230, y=510)

    submit = Button(patient_login, text="Login", height=2, width=15, font=('Arial', 20), command=check_login)
    submit.place(x=500, y=510)
    patient_login.bind("<Return>", check_login)


login_page()
patient_login.mainloop()
