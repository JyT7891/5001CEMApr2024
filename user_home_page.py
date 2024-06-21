import sys
import time
from tkinter import messagebox
from tkinter import *
from PIL import Image, ImageTk
from fire_base import initializeFirebase, getClient
from run_script import run_script1
import os

def initialize_home_page():
    username = os.getenv('USERNAME')  # Retrieve the username from the environment variable

    if not username:
        print("Error: USERNAME environment variable not set.")
        sys.exit(1)

    home_page = Tk()
    home_page.minsize(1250, 790)
    home_page.resizable(False, False)
    home_page.title(f"Call A Doctor - {username}")

    conn = initializeFirebase()
    db = getClient()

    def fetch_clinics_from_firebase():
        clinics_ref = db.collection('clinic')
        docs = clinics_ref.stream()
        clinics = []
        for doc in docs:
            clinic = doc.to_dict()
            clinics.append(clinic)
        return clinics

    def fetch_user_appointments(username):
        try:
            user_doc = db.collection('user').document(username).get()
            if user_doc.exists:
                user_data = user_doc.to_dict()
                return user_data.get('appointments', [])
            else:
                messagebox.showerror("User Not Found", "No user found with the specified username.")
                return []
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            return []

    def open_home():
        clear_content()

        content_frame = Frame(content_area, bg='white')
        content_frame.pack(fill='both', expand=True)

        about_frame = Frame(content_frame, bg='white', padx=20, pady=10)
        about_frame.grid(row=1, column=0, sticky='nsew')
        about_us_frame(about_frame)

        carousel_frame = Frame(content_frame, bg="white", width=400, height=400)
        carousel_frame.grid(row=0, column=0, padx=20, pady=10, sticky='nsew')
        load_images(carousel_frame)

    def load_images(slide_show_frame):
        image_files = ["carousel1.jpg", "carousel2.jpg", "carousel3.jpg"]

        images = []
        for img_file in image_files:
            try:
                image = Image.open(img_file)
                resized_image = image.resize((400, 400))
                photo_image = ImageTk.PhotoImage(resized_image)
                images.append(photo_image)
            except IOError as e:
                print(f"Error loading image {img_file}: {e}")

        current_image_label = Label(slide_show_frame, bg="white")
        current_image_label.pack()

        idx = 0
        transition_duration = 2000

        def update_image():
            nonlocal idx
            current_image_label.config(image=images[idx])
            idx = (idx + 1) % len(images)
            slide_show_frame.after(transition_duration, update_image)

        update_image()

    def about_us_frame(about_frame):
        about_text = """
            Welcome to Call A Doctor!

            Call A Doctor is committed to providing high-quality healthcare services to our patients. 
            Whether you need to search for clinics, book appointments, or manage your appointments, 
            our platform is here to assist you every step of the way.

            Our dedicated team works tirelessly to ensure that you receive the best possible care. 
            Thank you for choosing Call A Doctor as your partner in health!

            For any inquiries or assistance, please feel free to contact us.
            """
        about_label = Label(about_frame, text=about_text, justify='left', anchor='n', background='white',
                            font=('Helvetica', 15), fg='#07497d')
        about_label.grid(row=0, column=0, padx=20, pady=10, sticky='nsew')

        about_frame.grid_rowconfigure(0, weight=1)
        about_frame.grid_columnconfigure(0, weight=1)

    def book_appointment():
        clear_content()
        text = Label(content_area, text="Book Appointment", font=('Helvetica', 25, 'bold'), fg='#07497d')
        text.pack()
        text.pack(pady=10)
        clinics = fetch_clinics_from_firebase()

        def button_command(clinic_id):
            home_page.withdraw()
            run_script1('show_map.py', clinic_id, username)  # Pass username as well

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
        for idx, clinic in enumerate(clinics):
            row = idx // num_columns
            column = idx % num_columns
            clinic_frame = Frame(scrollable_frame, bd=0, relief="groove", padx=10, pady=10, bg="#f0f0f0",
                                 width=frame_width, height=frame_height)
            clinic_frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
            clinic_name_label = Label(clinic_frame, text=clinic['name'], font=('Helvetica', 15, 'bold'), bg="#f0f0f0",
                                      fg='#07497d')
            clinic_name_label.pack(anchor="w")
            clinic_num_label = Label(clinic_frame, text=clinic['phone_num'], font=('Helvetica', 12), bg="#f0f0f0",
                                     fg='#07497d')
            clinic_num_label.pack(anchor="w")
            open_time_label = Label(clinic_frame, text=f"Open Time: {clinic['open_time']}", font=('Helvetica', 12),
                                    bg="#f0f0f0", fg='#07497d')
            open_time_label.pack(anchor="w", pady=2)
            close_time_label = Label(clinic_frame, text=f"Close Time: {clinic['close_time']}", font=('Helvetica', 12),
                                     bg="#f0f0f0", fg='#07497d')
            close_time_label.pack(anchor="w", pady=2)
            clinic_frame.bind("<Button-1>", lambda event, clinic_id=clinic['clinic_id']: button_command(clinic_id))
            clinic_frame.pack_propagate(False)

    def my_appointments():
        clear_content()
        text = Label(content_area, text="My Appointments", font=('Helvetica', 25, 'bold'), fg='#07497d')
        text.pack()

        appointments = fetch_user_appointments(username)
        if not appointments:
            messagebox.showinfo("No Appointments", "You have no appointments.")
            return

        def view_details(appointment):
            details = f"Clinic: {appointment['clinic_name']}\n" \
                      f"Date: {appointment['date']}\n" \
                      f"Time: {appointment['time']}\n" \
                      f"Doctor: {appointment['doc_id']}\n" \
                      f"Patient: {appointment['patient_name']}"
            messagebox.showinfo("Appointment Details", details)

        def cancel_appointment(appointment):
            try:
                user_doc_ref = db.collection('user').document(username)
                user_doc = user_doc_ref.get()
                if user_doc.exists:
                    user_data = user_doc.to_dict()
                    user_data['appointments'] = [appt for appt in user_data['appointments'] if appt != appointment]
                    user_doc_ref.set(user_data)
                    messagebox.showinfo("Cancelled", "Appointment cancelled successfully.")
                    my_appointments()  # Refresh the appointments list
                else:
                    messagebox.showerror("Error", "User document not found.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

        canvas = Canvas(content_area, bg="white")
        scrollbar = Scrollbar(content_area, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas, bg="white")
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        for idx, appointment in enumerate(appointments):
            appointment_frame = Frame(scrollable_frame, bd=1, relief="solid", padx=10, pady=10, bg="#f0f0f0")
            appointment_frame.pack(padx=10, pady=10, fill='x')

            clinic_label = Label(appointment_frame, text=f"Clinic: {appointment['clinic_name']}", font=('Helvetica', 15, 'bold'), bg="#f0f0f0", fg='#07497d')
            clinic_label.pack(anchor="w")
            date_label = Label(appointment_frame, text=f"Date: {appointment['date']}", font=('Helvetica', 12), bg="#f0f0f0", fg='#07497d')
            date_label.pack(anchor="w")
            time_label = Label(appointment_frame, text=f"Time: {appointment['time']}", font=('Helvetica', 12), bg="#f0f0f0", fg='#07497d')
            time_label.pack(anchor="w")
            doc_label = Label(appointment_frame, text=f"Doctor: {appointment['doc_id']}", font=('Helvetica', 12), bg="#f0f0f0", fg='#07497d')
            doc_label.pack(anchor="w")

            details_button = Button(appointment_frame, text="View Details", command=lambda a=appointment: view_details(a))
            details_button.pack(side=LEFT, padx=5)

            cancel_button = Button(appointment_frame, text="Cancel", command=lambda a=appointment: cancel_appointment(a))
            cancel_button.pack(side=LEFT, padx=5)

    def clear_content():
        for widget in content_area.winfo_children():
            widget.destroy()

    nav_frame = Frame(home_page, width=200, bg='#2a2a2a')
    nav_frame.pack(fill='y', side='left')

    content_area = Frame(home_page, bg='white')
    content_area.pack(fill='both', expand=True)

    about_us_btn = Button(nav_frame, text="Home", font=('Helvetica', 20), fg='white', bg='#2a2a2a', command=open_home,
                          relief='flat')
    about_us_btn.pack(fill='x')

    clinic_btn = Button(nav_frame, text="Search Clinics", font=('Helvetica', 20), fg='white', bg='#2a2a2a',
                        command=lambda: book_appointment(), relief='flat')
    clinic_btn.pack(fill='x')

    book_btn = Button(nav_frame, text="Book Appointment", font=('Helvetica', 20), fg='white', bg='#2a2a2a',
                      command=book_appointment, relief='flat')
    book_btn.pack(fill='x')

    appointments_btn = Button(nav_frame, text="My Appointments", font=('Helvetica', 20), fg='white', bg='#2a2a2a',
                              command=my_appointments, relief='flat')
    appointments_btn.pack(fill='x')

    open_home()
    home_page.mainloop()

if __name__ == "__main__":
    initialize_home_page()
