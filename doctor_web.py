from tkinter import *
from tkinter import messagebox
from datetime import datetime
from run_script import run_script1
from fire_base import getClient, initializeFirebase

# Initialize the Firebase Admin SDK
conn = initializeFirebase()
db = getClient()

# Global list to store appointments
appointments = []

# Initialize Tkinter
doctor = Tk()
doctor.title("Doctor Appointment System")
doctor.minsize(1250, 790)
doctor.resizable(False, False)


def clock_in_out():
    messagebox.showinfo("Clock In/Out", "Feature under development")


def check_appointment():
    clear_content()

    # Example: Query appointments from Firebase Firestore
    appointments_ref = db.collection('appointments').get()
    appointments.clear()

    for appointment in appointments_ref:
        appointments.append(appointment.to_dict())

    if appointments:
        # Display appointments in content_area
        for idx, appointment in enumerate(appointments, start=1):
            appointment_text = f"Appointment {idx}: \n"
            appointment_text += f"Patient: {appointment['patient_name']}\n"
            appointment_text += f"Time: {appointment['appointment_time']}\n"
            appointment_text += f"Doctor: {appointment['doctor']}\n\n"

            label = Label(content_area, text=appointment_text, font=('Helvetica', 12))
            label.pack(anchor="w", pady=10)
    else:
        label = Label(content_area, text="No appointments found.", font=('Helvetica', 12))
        label.pack(anchor="w", pady=10)


def open_profile():
    clear_content()

    # Example: Query doctor profiles from Firebase Firestore
    doctors_ref = db.collection('doctors').get()

    for doctor in doctors_ref:
        doctor_data = doctor.to_dict()
        profile_text = f"Doctor Name: {doctor_data['name']}\n"
        profile_text += f"Specialty: {doctor_data['specialty']}\n"
        profile_text += f"Location: {doctor_data['location']}\n\n"

        label = Label(content_area, text=profile_text, font=('Helvetica', 12))
        label.pack(anchor="w", pady=10)


def log_out():
    # Clear the content area
    doctor.destroy()
    run_script1('login_page.py')


def clear_content():
    # Clear the content area
    for widget in content_area.winfo_children():
        widget.destroy()


# Function to handle button appearance on hover and click
def on_enter(event):
    event.widget.config(width=19, height=2, font=('Helvetica', 12, 'bold'))


def on_leave(event):
    event.widget.config(width=20, height=2, font=('Helvetica', 10))


def on_click(event):
    event.widget.config(bg="blue")


def on_release(event):
    event.widget.config(bg="SystemButtonFace")


# Function to create and pack buttons with events
def create_button(text, command):
    button = Button(sidebar, text=text, command=command, width=20, height=2, font=('Helvetica', 10))
    button.pack(pady=20)
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)
    button.bind("<ButtonPress-1>", on_click)
    button.bind("<ButtonRelease-1>", on_release)
    return button


# Create a Frame for the sidebar
sidebar = Frame(doctor, width=200, bg="lavender")
sidebar.pack(fill=Y, side=LEFT)

# Load and display the logo
logo_image = PhotoImage(file="cad1.png")
logo_label = Label(sidebar, image=logo_image, bg="lavender")
logo_label.pack(pady=10, padx=10)

# Main content area
content_area = Frame(doctor, bg="white", padx=20, pady=20)
content_area.pack(expand=True, fill="both", side=RIGHT)

# Create buttons for navigation in the sidebar
create_button("Clock In Out", clock_in_out)
create_button("Appointment", check_appointment)
create_button("Profile", open_profile)
create_button("Log Out", log_out)

# Start the main loop
doctor.mainloop()
