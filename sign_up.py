from datetime import datetime
import calendar
from tkinter import *
import tkinter as tk
import PIL
from PIL import Image, ImageTk
from tkinter.ttk import Combobox
from tkinter import messagebox
from fire_base import getClient, initializeFirebase
from run_script import run_script1

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
    calculate()

    # Get the values from the entry fields
    username = insert_username.get()
    name = insert_name.get()
    password = insert_password.get()
    gender = gender_type_combobox.get()
    blood = blood_type_var.get()
    year = year1
    month = month1
    day = day1
    age = age1

    # Initialize Firebase connection
    conn = initializeFirebase()
    db = getClient()

    docRef = db.collection('user').document(username)
    docRef.set({
        'username': username,
        'name': name,
        'age': age,
        'password': password,
        'gender': gender,
        'bloodType': blood,
        'year': year,
        'month': month,
        'day': day,
        'userType': 'user'  # Set the default user type to 'user'
    })

    messagebox.showinfo("Success", "Sign up successful!")
    patient_sign_up.destroy()
    run_script1('login_page.py')


def call_back():
    patient_sign_up.destroy()
    run_script1('login_page.py')


def sign():
    global insert_username, insert_name, insert_password, gender_type_combobox, blood_type_var
    username = Label(patient_sign_up, text="Username         :", font=('Arial', 20))
    username.place(x=150, y=180)
    insert_username = Entry(patient_sign_up, width=30, font='Arial 19')
    insert_username.place(x=380, y=180)

    age = Label(patient_sign_up, text="Date of Birth     :", font=('Arial', 20))
    age.place(x=150, y=260)
    generate_years()
    date_of_birth()

    name = Label(patient_sign_up, text="Name                :", font=('Arial', 20))
    name.place(x=150, y=340)
    insert_name = Entry(patient_sign_up, width=30, font=('Arial', 19))
    insert_name.place(x=380, y=340)

    password = Label(patient_sign_up, text="Password          :", font=('Arial', 20))
    password.place(x=150, y=420)
    insert_password = Entry(patient_sign_up, width=30, font=('Arial', 19))
    insert_password.place(x=380, y=420)

    gender = Label(patient_sign_up, text="Gender              :", font=('Arial', 20))
    gender.place(x=150, y=510)
    gender_types = ["Male", "Female"]
    gender_type_combobox = Combobox(patient_sign_up, values=gender_types, font=('Arial', 19), state='readonly')
    gender_type_combobox.place(x=380, y=510)

    blood_type = Label(patient_sign_up, text="Blood Type        :", font=('Arial', 20))
    blood_type.place(x=150, y=600)
    blood_types = ["A", "B", "AB", "O"]
    blood_type_var = StringVar()
    for i, blood_type_option in enumerate(blood_types):
        blood_type_radio = Radiobutton(patient_sign_up, text=blood_type_option, variable=blood_type_var,
                                       value=blood_type_option, font=('Arial', 19))
        blood_type_radio.place(x=380 + i * 100, y=600)

    submit = Button(patient_sign_up, text="Sign Up", height=2, width=15, font=('Arial', 20), command=check_sign_up)
    submit.place(x=550, y=690)

    cancel = Button(patient_sign_up, text="Cancel", height=2, width=15, font=('Arial', 20), command=call_back)
    cancel.place(x=200, y=690)


def generate_years():
    current_year = datetime.now().year
    return [str(year) for year in range(current_year, current_year - 100, -1)]


def date_of_birth():
    global year_var, month_var, day_var, day_combobox
    # Labels
    year_label = Label(patient_sign_up, text="Year:", font=('Arial', 16))
    year_label.place(x=320, y=260)
    month_label = Label(patient_sign_up, text="Month:", font=('Arial', 16))
    month_label.place(x=480, y=260)
    day_label = Label(patient_sign_up, text="Day:", font=('Arial', 16))
    day_label.place(x=620, y=260)

    # Years Dropdown List (Combobox)
    years = list(range(1900, datetime.now().year + 1))
    year_var = tk.StringVar()
    year_combobox = Combobox(patient_sign_up, textvariable=year_var, values=years, state="readonly", width=5,
                             font=('Arial', 16))
    year_combobox.place(x=380, y=260)
    year_combobox.current(len(years) - 1)
    year_combobox.bind("<<ComboboxSelected>>", update_days)

    # Months Dropdown List (Combobox)
    months = list(range(1, 13))
    month_var = tk.StringVar()
    month_combobox = Combobox(patient_sign_up, textvariable=month_var, values=months, state="readonly", width=3,
                              font=('Arial', 16))
    month_combobox.place(x=540, y=260)
    month_combobox.current(0)
    month_combobox.bind("<<ComboboxSelected>>", update_days)

    # Days Dropdown List (Combobox)
    days = list(range(1, 32))
    day_var = tk.StringVar()
    day_combobox = Combobox(patient_sign_up, textvariable=day_var, values=days, state="readonly", width=3,
                            font=('Arial', 16))
    day_combobox.place(x=680, y=260)
    day_combobox.current(0)


def update_days(event):
    year = int(year_var.get())
    month = int(month_var.get())

    if month == 0:
        month = 1

    days_in_month = calendar.monthrange(year, month)[1]
    days = list(range(1, days_in_month + 1))
    day_combobox['values'] = days
    if int(day_var.get()) not in days:
        day_combobox.current(0)  # Set to the first day if the current day is not valid


def calculate():
    global year1, month1, day1, age1
    try:
        year1 = int(year_var.get())
        month1 = int(month_var.get())
        day1 = int(day_var.get())

        birth_date = datetime(year1, month1, day1)
        current_date = datetime.now()

        age1 = current_date.year - birth_date.year - (
                (current_date.month, current_date.day) < (birth_date.month, birth_date.day))

        print(f"Calculated Age: {age1}")

    except ValueError:
        messagebox.showwarning("Input Error", "Please select valid Year, Month, and Day.")


sign()
patient_sign_up.mainloop()
