from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
# Import the function from run_script.py
from run_script import run_script1

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
    username1 = insert_email.get()  # Get the text from the username field
    print("Username:", username1)
    # password1 = insert_password.get()
    # if correct run into homepage
    patient_login.destroy()
    run_script1('home_page.py')
    # else sign up page


def check_sign_up():
    # Close the current Tkinter window
    patient_login.destroy()
    # Call the function to run the script
    run_script1('sign_up.py')


def login_page():
    global insert_email, insert_password
    email = Label(patient_login, text="Email           : ", font=('Arial', 20))
    email.place(x=200, y=310)
    insert_email = Entry(patient_login, width=30, font='Arial 19')
    insert_email.place(x=380, y=310)

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


login_page()
patient_login.mainloop()
