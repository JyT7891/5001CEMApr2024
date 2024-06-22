# Create a Toplevel window for adding a user
from calendar import calendar
from datetime import date
from tkinter import *
from tkinter.ttk import Combobox

from tkinter import *
from tkinter import ttk


def edit_user(user_data):
    edit_user_window = Tk()
    edit_user_window.title("Edit User")
    edit_user_window.minsize(500, 300)
    edit_user_window.resizable(False, False)

    # Name
    Label(edit_user_window, text="Name         :", font=('Helvetica', 12)).place(x=50, y=50)
    name_entry = Entry(edit_user_window, width=25, font='Arial 15')
    name_entry.place(x=150, y=50)
    name_entry.insert(0, user_data['name'])

    # Gender
    Label(edit_user_window, text="Gender        :", font=('Helvetica', 12)).place(x=50, y=100)
    gender_var = StringVar(edit_user_window)
    gender_var.set(user_data['gender'])  # Set default value
    gender_dropdown = OptionMenu(edit_user_window, gender_var, "Male", "Female")
    gender_dropdown.config(width=20, font=('Arial', 12))
    gender_dropdown.place(x=150, y=100)

    # Blood Type
    Label(edit_user_window, text="Blood Type  :", font=('Helvetica', 12)).place(x=50, y=150)
    blood_type_var = StringVar(edit_user_window)
    blood_type_var.set(user_data['bloodType'])  # Set default value
    blood_type_dropdown = OptionMenu(edit_user_window, blood_type_var, "O", "A", "B", "AB")
    blood_type_dropdown.config(width=18, font=('Arial', 12))
    blood_type_dropdown.place(x=150, y=150)

    # Submit Button
    submit_button = Button(edit_user_window, text="Update", command=lambda: submit_user_update, height=1,
                           width=10,
                           font=('Arial', 12))
    submit_button.place(x=200, y=230)

    edit_user_window.mainloop()


def submit_user_update():
    pass


# Example usage:
user_data = {'name': 'John Doe', 'gender': 'Male', 'bloodType': 'O'}
edit_user(user_data)
