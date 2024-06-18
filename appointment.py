import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Combobox

from tkcalendar import Calendar
from fire_base import getClient, initializeFirebase
from run_script import run_script1

# Initialize the Firebase Admin SDK
conn = initializeFirebase()
db = getClient()

# Create the main Tkinter window
clinic = tk.Tk()
clinic.minsize(700, 600)
clinic.resizable(False, False)
clinic.title("Clinic Name")

# Clinic name label
clinic_name = tk.Label(clinic, text="Clinic Name", font=('Helvetica', 25, 'bold'))
clinic_name.place(x=250, y=50)

# Doctor list label and dropdown
doctor_label = tk.Label(clinic, text="Select Doctor    :", font=('Helvetica', 14))
doctor_label.place(x=100, y=150)

doctor_var = tk.StringVar(clinic)
doctor_list = ["Dr. Smith", "Dr. Johnson", "Dr. Williams"]  # Example doctors
doctor_menu = tk.OptionMenu(clinic, doctor_var, *doctor_list)
doctor_menu.place(x=300, y=150)

# Set the width of the OptionMenu
doctor_menu.config(width=20)  # Adjust the width here

# Calendar widget with improved styling
calendar_label = tk.Label(clinic, text="Select Date       :", font=('Helvetica', 14))
calendar_label.place(x=100, y=210)

# Customizing the calendar appearance
calendar_style = {'background': 'lightgray', 'foreground': 'black',
                  'borderwidth': 2, 'highlightthickness': 0,
                  'padding': 10, 'font': ('Helvetica', 12)}

calendar = Calendar(clinic, selectmode='day', date_pattern='yyyy-mm-dd', **calendar_style)
calendar.place(x=300, y=210)

# Time entry widgets
time_label = tk.Label(clinic, text="Select Time      :", font=('Helvetica', 14))
time_label.place(x=100, y=450)

# Generate time options in 5-minute intervals
hours = [f"{i:02d}" for i in range(24)]
minutes = [f"{i:02d}" for i in range(0, 60, 5)]
time_options = [f"{hour}:{minute}" for hour in hours for minute in minutes]

time_var = tk.StringVar()
time_menu = Combobox(clinic, textvariable=time_var, values=time_options, state="readonly", width=10,
                     font=('Helvetica', 12))
time_menu.place(x=300, y=450)


# Appointment submission
def submit_appointment():
    doctor = doctor_var.get()
    date = calendar.get_date()
    time = time_var.get()

    if not doctor or not time:
        messagebox.showerror("Invalid Input", "Please select a doctor and a time.")
        return

    appointment = {
        "doc_id": doctor,
        "date": date,
        "time": time
    }

    # Save appointment to Firebase
    db.collection('appointments').add(appointment)

    messagebox.showinfo("Appointment Added", f"Appointment with {doctor} on {date} at {time} added.")

    # Clear the inputs
    doctor_var.set('')
    time_var.set('')
    back()


def back():
    run_script1("user_home_page.py")


# Submit button
submit_button = tk.Button(clinic, text="Submit", command=submit_appointment)
submit_button.place(x=250, y=500)

# Cancel Button
cancel_button = tk.Button(clinic, text="Cancel", command=back)
cancel_button.place(x=350, y=500)

clinic.mainloop()
