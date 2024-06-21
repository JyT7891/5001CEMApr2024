import sys
import os
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from fire_base import initializeFirebase, getClient
from run_script import run_script1

admin_clinic = Tk()
admin_clinic.minsize(1300, 790)
admin_clinic.resizable(False, False)
admin_clinic.title("Call A Doctor Admin Page ")

# Create the header frame
header_frame = Frame(admin_clinic, bg='#07497d', height=100)
header_frame.pack(fill=X)
header_label = Label(header_frame, text="Call A Doctor", font=('Helvetica', 35, 'bold'), bg='#07497d',
                     fg='white')
header_label.pack(side=LEFT, padx=20)
contact_label = Label(header_frame, text="Contact Us: +1 234 567 890 | email@example.com",
                      font=('Helvetica', 15),
                      bg='#07497d', fg='white')
contact_label.pack(side=RIGHT, padx=20)


def clinic_list():
    pass


def doctor_list():
    pass


def patient_list():
    pass


def log_out():
    admin_clinic.destroy()
    run_script1('login_page.py')


def clear_content():
    for widget in content_area.winfo_children():
        widget.destroy()


def on_enter(event):
    event.widget.config(bg='#07497d')


def on_leave(event):
    event.widget.config(bg='#2a2a2a')


def create_nav_button(text, command):
    button = Button(nav_frame, text=text, font=('Helvetica', 20), fg='white', bg='#2a2a2a', command=command,
                    relief='flat')
    button.pack(fill='x', padx=20, pady=10)  # Adjusted padx and pady for spacing
    button.bind("<Enter>", on_enter)  # Bind on_enter function to mouse enter event
    button.bind("<Leave>", on_leave)  # Bind on_leave function to mouse leave event


nav_frame = Frame(admin_clinic, width=200, bg='#2a2a2a')
nav_frame.pack(fill='y', side='left')

content_area = Frame(admin_clinic, bg='white')
content_area.pack(fill='both', expand=True)

# create_nav_button("Home", open_home_page)
create_nav_button("Clinic List", clinic_list)
create_nav_button("Doctor List", doctor_list)
create_nav_button("Patient List", patient_list)
create_nav_button("Log Out", log_out)

conn = initializeFirebase()
db = getClient()

admin_clinic.mainloop()
