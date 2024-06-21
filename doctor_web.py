import os
import sys
from tkinter import *
from tkinter import messagebox
from datetime import datetime
from run_script import run_script1
from fire_base import getClient, initializeFirebase
from PIL import Image, ImageTk

# Initialize the Firebase Admin SDK
conn = initializeFirebase()
db = getClient()


def doctor_website(username):
    doctor = Tk()
    doctor.minsize(1250, 790)
    doctor.resizable(False, False)
    doctor.title(f"Doctor Appointment System - {username}")

    # Create the header frame
    header_frame = Frame(doctor, bg='#07497d', height=100)
    header_frame.pack(fill=X)
    header_label = Label(header_frame, text="Call A Doctor", font=('Helvetica', 35, 'bold'), bg='#07497d',
                         fg='white')
    header_label.pack(side=LEFT, padx=20)
    contact_label = Label(header_frame, text="Contact Us: +1 234 567 890 | email@example.com",
                          font=('Helvetica', 15),
                          bg='#07497d', fg='white')
    contact_label.pack(side=RIGHT, padx=20)

    def clock_in_out():
        try:
            # Fetch current doctor document from Firestore
            doctor_ref = db.collection('doctor').document(username)
            doctor_doc = doctor_ref.get()

            if doctor_doc.exists:
                doctor_data = doctor_doc.to_dict()
                current_status = doctor_data.get('is_Available',
                                                 False)  # Default to False if 'is_Available' doesn't exist

                # Toggle the 'is_Available' status
                new_status = not current_status  # Toggle the boolean value

                # Update the document with the new 'is_Available' status
                doctor_ref.update({
                    'is_Available': new_status
                })

                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if new_status:
                    status_msg = "available"
                else:
                    status_msg = "unavailable"

                messagebox.showinfo("Availability Update", f"You are now {status_msg} at {current_time}")

            else:
                messagebox.showerror("Error", "Doctor profile not found.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def check_appointment():
        clear_content()

        def check_appointment_button():
            doctor.destroy()
            run_script1('patient_report.py', username)

        try:
            doctor_ref = db.collection('doctor').document(username).get()
            if doctor_ref.exists:
                doctor_data = doctor_ref.to_dict()
                appointments_array = doctor_data.get('appointments', [])

                if appointments_array:
                    canvas = Canvas(content_area, bg="white")
                    scrollbar = Scrollbar(content_area, orient="vertical", command=canvas.yview)
                    scrollable_frame = Frame(canvas, bg="white")

                    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
                    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                    canvas.configure(yscrollcommand=scrollbar.set)

                    canvas.pack(side=LEFT, fill=BOTH, expand=True)
                    scrollbar.pack(side=RIGHT, fill=Y)

                    frame_width = 300
                    frame_height = 150
                    num_columns = 3

                    for idx, appointment_data in enumerate(appointments_array):
                        row = idx // num_columns
                        column = idx % num_columns
                        appointment_frame = Frame(scrollable_frame, bd=0, relief="groove", padx=10, pady=10,
                                                  bg="#f0f0f0",
                                                  width=frame_width, height=frame_height)
                        appointment_frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

                        patient_label = Label(appointment_frame,
                                              text=f"Patient: {appointment_data.get('patient_name', 'N/A')}",
                                              font=('Helvetica', 15, 'bold'), bg="#f0f0f0", fg='#07497d')
                        patient_label.pack(anchor="w")

                        date_label = Label(appointment_frame, text=f"Date: {appointment_data.get('date', 'N/A')}",
                                           font=('Helvetica', 12), bg="#f0f0f0", fg='#07497d')
                        date_label.pack(anchor="w")

                        time_label = Label(appointment_frame, text=f"Time: {appointment_data.get('time', 'N/A')}",
                                           font=('Helvetica', 12), bg="#f0f0f0", fg='#07497d')
                        time_label.pack(anchor="w", pady=2)

                        doctor_label = Label(appointment_frame, text=f"Doctor: {appointment_data.get('doc_id', 'N/A')}",
                                             font=('Helvetica', 12), bg="#f0f0f0", fg='#07497d')
                        doctor_label.pack(anchor="w", pady=2)

                        appointment_frame.bind("<Button-1>",
                                               lambda event, app=appointment_data: check_appointment_button())
                        appointment_frame.pack_propagate(False)
                else:
                    label = Label(content_area, text="No appointments found.", font=('Helvetica', 12))
                    label.pack(anchor="w", pady=10)
            else:
                messagebox.showerror("Error", "Doctor profile not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch appointments: {str(e)}")

    def get_clinic_name(clinic_id):
        try:
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

    def open_home_page():
        clear_content()

        content_frame = Frame(content_area, bg='white')
        content_frame.pack(fill='both', expand=True)

        doctor_ref = db.collection('doctor').document(username).get()
        doctor_data = doctor_ref.to_dict()
        clinic_name = get_clinic_name(doctor_data['clinic_id'])
        if doctor_ref.exists:
            profile_text = f"Welcome, {doctor_data['doc_name']}!\n\n"
            profile_text += f"Clinic Name: {clinic_name}\n"
            profile_text += f"Service: {doctor_data['service']}\n"

            label = Label(content_frame, text=profile_text, font=('Helvetica', 14, 'bold'), background='white')
            label.pack(anchor="center", pady=50)
        else:
            label = Label(content_frame, text="Doctor profile not found.", font=('Helvetica', 12))
            label.pack(anchor="center", pady=50)

    def log_out():
        doctor.destroy()
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

    nav_frame = Frame(doctor, width=200, bg='#2a2a2a')
    nav_frame.pack(fill='y', side='left')

    content_area = Frame(doctor, bg='white')
    content_area.pack(fill='both', expand=True)

    create_nav_button("Home", open_home_page)
    create_nav_button("Clock In Out", clock_in_out)
    create_nav_button("Appointment", check_appointment)
    create_nav_button("Log Out", log_out)

    open_home_page()
    doctor.mainloop()


if __name__ == '__main__':
    username = os.getenv('USERNAME')
    if not username:
        print("Error: USERNAME environment variable not set")
        sys.exit(1)

    doctor_website(username)
