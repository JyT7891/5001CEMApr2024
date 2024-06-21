import sys
from tkinter import *
from tkinter import messagebox
from datetime import datetime
from run_script import run_script1, show_clinic_patient
from fire_base import getClient, initializeFirebase

# Initialize the Firebase Admin SDK
conn = initializeFirebase()
db = getClient()

# Global list to store appointments
appointments = []


def doctor_website(username):
    # Initialize Tkinter
    doctor = Tk()
    doctor.title(f"Doctor Appointment System - {username}")
    doctor.minsize(1250, 790)
    doctor.resizable(False, False)

    def clock_in_out():
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        messagebox.showinfo("Clock In/Out", f"You have clocked in/out at {current_time}")
        doctor_ref = db.collection('doctor').document(username).get()

        # Example: Update Firebase with clock-in/out time
        # Assuming you have a 'doctors' collection with a document for each doctor
        doctor_id = username # Replace with actual doctor ID
        doctor_ref = db.collection('doctors').document(doctor_id)
        doctor_ref.update({
            'last_clock_time': current_time,
            'clocked_in': True,  # Or False for clock out
        })

    def check_appointment():
        clear_content()

        def check_appointment_button():
            doctor.destroy()
            run_script1('patient_report.py', username)

        try:
            # Fetch doctor document to get appointments array
            doctor_ref = db.collection('doctor').document(username).get()
            if doctor_ref.exists:
                doctor_data = doctor_ref.to_dict()

                # Extract appointments array from doctor_data
                appointments_array = doctor_data.get('appointments', [])

                if appointments_array:
                    # Create a scrollable canvas
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

                        date_label = Label(appointment_frame, text=f"Date    :  {appointment_data.get('date', 'N/A')}",
                                           font=('Helvetica', 12), bg="#f0f0f0", fg='#07497d')
                        date_label.pack(anchor="w")

                        time_label = Label(appointment_frame, text=f"Time    :  {appointment_data.get('time', 'N/A')}",
                                           font=('Helvetica', 12), bg="#f0f0f0", fg='#07497d')
                        time_label.pack(anchor="w", pady=2)

                        doctor_label = Label(appointment_frame, text=f"Doctor :  {appointment_data.get('doc_id', 'N/A')}",
                                             font=('Helvetica', 12), bg="#f0f0f0", fg='#07497d')
                        doctor_label.pack(anchor="w", pady=2)

                        appointment_frame.bind("<Button-1>", lambda: check_appointment_button)
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

    def open_home_page():
        clear_content()

        content_frame = Frame(content_area, bg='white')
        content_frame.pack(fill='both', expand=True)

        # Example: Query doctor profile from Firebase Firestore using the username
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
    create_button("Log Out", log_out)

    open_home_page()

    # Start the main loop
    doctor.mainloop()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python doctor_web.py <username>")

    username = sys.argv[1]
    doctor_website(username)
