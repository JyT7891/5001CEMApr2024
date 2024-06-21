import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from tkinter.ttk import Combobox
from tkcalendar import Calendar
from firebase_admin import firestore
from fire_base import getClient, initializeFirebase
from run_script import run_script1
import sys

# Initialize the Firebase Admin SDK
conn = initializeFirebase()
db = getClient()


# Function to submit appointment
def submit_appointment():
    doctor = doctor_var.get()
    date = calendar.get_date()
    time = time_var.get()

    if not doctor or not time:
        messagebox.showerror("Invalid Input", "Please select a doctor and a time.")
        return

    # Validate date and time
    if not validate_datetime():
        return

    try:
        # Fetch doctor document based on the selected doctor's name
        doctor_query = db.collection('doctor').where('doc_name', '==', doctor).limit(1).get()
        doctor_id = None

        for doc in doctor_query:
            doctor_id = doc.id
            clinic_id = doc.to_dict().get('clinic_id')
            break  # Assuming there's only one doctor with a given name, break after finding it

        if not doctor_id:
            messagebox.showerror("Error", f"Doctor '{doctor}' not found.")
            return
        
        # Construct the appointment data
        appointment_data = {
            "clinic_name": clinic_id,  # Assuming clinic_id is defined elsewhere
            'patient_name': username,
            "doc_id": doctor,
            "date": date,
            "time": time
        }

        # Save appointment to Firestore under 'username' (replace with actual username)
        user_doc_ref = db.collection('user').document(username)
        user_doc_ref.update({
            'appointments': firestore.ArrayUnion([appointment_data])
        })

        # Save appointment to doctor's appointment list
        doctor_doc_ref = db.collection('doctor').document(doctor_id)
        doctor_doc_ref.update({
            'appointments': firestore.ArrayUnion([appointment_data])
        })

        # Show success message
        messagebox.showinfo("Appointment Added", f"Appointment with {doctor} on {date} at {time} added successfully.")

        back()

    except Exception as e:
        # Show error message if any exception occurs
        messagebox.showerror("Error", f"Failed to add appointment: {e}")


def back():
    clinic.destroy()
    run_script1("user_home_page.py", username)


def getDoctorByClinicID(clinic_id):
    try:
        # Fetch doctors using clinic ID
        doctor_docs = db.collection('doctor').where('clinic_id', '==', clinic_id).get()
        doctor_list = [doc.to_dict()['doc_name'] for doc in doctor_docs]
        return doctor_list

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        return []


def getClinicName(clinic_id):
    try:
        # Fetch clinic document using clinic ID
        clinic_doc = db.collection('clinic').document(clinic_id).get()
        if clinic_doc.exists:
            clinic_data = clinic_doc.to_dict()
            return clinic_data.get('name')
        else:
            messagebox.showerror("Clinic Not Found", "No clinic found with the specified ID.")
            return None
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        return None


# Function to validate date and time
def validate_datetime():
    selected_date = calendar.get_date()
    selected_time = time_var.get()

    # Convert selected date and time to datetime objects
    selected_datetime = datetime.strptime(f"{selected_date} {selected_time}", "%Y-%m-%d %H:%M")

    # Get current date and time
    current_datetime = datetime.now()

    # Check if selected datetime is in the past
    if selected_datetime < current_datetime:
        tk.messagebox.showerror("Invalid Selection", "Please select a future date and time.")
        return False
    else:
        return True


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python show_map.py <clinic_id>")
        sys.exit(1)
    clinic_id = sys.argv[1]
    username = sys.argv[2]

    # Create the main Tkinter window
    clinic = tk.Tk()
    clinic.minsize(700, 600)
    clinic.resizable(False, False)
    clinic.title(getClinicName(clinic_id))

    # Clinic name label
    clinic_name_label = tk.Label(clinic, text=f"Clinic Name : {getClinicName(clinic_id)}",
                                 font=('Helvetica', 15, 'bold'))
    clinic_name_label.place(x=250, y=50)

    # Doctor list label and dropdown
    doctor_label = tk.Label(clinic, text="Select Doctor    :", font=('Helvetica', 14))
    doctor_label.place(x=100, y=150)

    global doctor_var
    doctor_var = tk.StringVar(clinic)
    doctor_list = getDoctorByClinicID(clinic_id)  # Get doctors based on clinic name
    doctor_menu = tk.OptionMenu(clinic, doctor_var, *doctor_list)
    doctor_menu.place(x=300, y=150)
    doctor_menu.config(width=20)

    # Calendar widget with improved styling
    calendar_label = tk.Label(clinic, text="Select Date       :", font=('Helvetica', 14))
    calendar_label.place(x=100, y=210)

    global calendar
    calendar_style = {'background': 'light gray', 'foreground': 'black',
                      'border width': 2, 'highlight thickness': 0,
                      'padding': 10, 'font': ('Helvetica', 12)}
    calendar = Calendar(clinic, selectmode='day', date_pattern='yyyy-mm-dd', **calendar_style)
    calendar.place(x=300, y=210)

    # Time entry widgets
    time_label = tk.Label(clinic, text="Select Time      :", font=('Helvetica', 14))
    time_label.place(x=100, y=450)

    global time_var
    hours = [f"{i:02d}" for i in range(24)]
    minutes = [f"{i:02d}" for i in range(0, 60, 5)]
    time_options = [f"{hour}:{minute}" for hour in hours for minute in minutes]
    time_var = tk.StringVar()
    time_menu = Combobox(clinic, textvariable=time_var, values=time_options, state="readonly", width=10,
                         font=('Helvetica', 12))
    time_menu.place(x=300, y=450)

    # Submit button
    submit_button = tk.Button(clinic, text="Submit", command=submit_appointment)
    submit_button.place(x=250, y=500)

    # Cancel Button
    cancel_button = tk.Button(clinic, text="Cancel", command=back)
    cancel_button.place(x=350, y=500)

    clinic.mainloop()
