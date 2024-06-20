import sys
import time
from tkinter import messagebox
from tkinter import *
from PIL import Image, ImageTk
from fire_base import initializeFirebase, getClient
from run_script import run_script1


def initialize_home_page(username):
    # Initialize the main window
    home_page = Tk()
    home_page.minsize(1250, 790)
    home_page.resizable(False, False)
    home_page.title(f"Call A Doctor - {username}")

    # Initialize the Firebase Admin SDK
    conn = initializeFirebase()
    db = getClient()

    def open_home():
        clear_content()

        # Create a frame for carousel and about us
        content_frame = Frame(content_area, bg='white')
        content_frame.pack(fill='both', expand=True)

        # About us on the left side with margin and smaller padding
        about_frame = Frame(content_frame, bg='white', padx=20, pady=10)
        about_frame.grid(row=1, column=0, sticky='nsew')
        about_us_frame(about_frame)

        # Load images carousel on the right side
        carousel_frame = Frame(content_frame, bg="white", width=400, height=400)
        carousel_frame.grid(row=0, column=0, padx=20, pady=10, sticky='nsew')
        load_images(carousel_frame)

    def load_images(slide_show_frame):
        image_files = ["carousel1.jpg", "carousel2.jpg", "carousel3.jpg"]  # Replace with your image filenames

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
        transition_duration = 2000  # Transition duration in milliseconds

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
        about_label.grid(row=0, column=0, padx=20, pady=10, sticky='nsew')  # Ensure sticky='nsew' to stick to top

        # Set row and column weights to allow resizing
        about_frame.grid_rowconfigure(0, weight=1)
        about_frame.grid_columnconfigure(0, weight=1)

    def fetch_clinics_from_firebase():
        clinics_ref = db.collection('clinic')
        docs = clinics_ref.stream()
        clinics = []
        for doc in docs:
            clinic = doc.to_dict()
            clinics.append(clinic)
        return clinics

    def book_appointment():
        clear_content()
        text = Label(content_area, text="Book Appointment", font=('Helvetica', 25, 'bold'), background="white",
                     fg='#07497d')
        text.pack(pady=10)
        clinics = fetch_clinics_from_firebase()

        def button_command(clinic_id):
            home_page.withdraw()
            messagebox.showinfo("Test", f"{clinic_id}")
            run_script1('show_map.py', clinic_id)

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

    def open_profile():
        # Clear the content area
        clear_content()

        profile_frame = Frame(content_area, background='white')
        profile_frame.pack(padx=50, pady=20)

        profile_label = Label(profile_frame, text="Profile", font=('Helvetica', 30, 'bold'), background='white')
        profile_label.pack()

        # Fetch patient data from the database
        try:
            doc = db.collection('user').document(username).get()
            if doc.exists:
                patient_info = doc.to_dict()
            else:
                patient_info = {'username': 'N/A', 'age': 'N/A', 'email': 'N/A', 'password': 'N/A', 'blood_type': 'N/A'}

            profile_data_frame = Frame(profile_frame, background='white')
            profile_data_frame.pack(padx=20, pady=20)

            # Labels for non-editable fields
            Label(profile_data_frame, text="Username       : ", font=('Helvetica', 15), bg='white').grid(row=0,
                                                                                                         column=0,
                                                                                                         sticky='w',
                                                                                                         padx=5,
                                                                                                         pady=5)
            Label(profile_data_frame, text=patient_info['username'], font=('Helvetica', 15), bg='white').grid(row=0,
                                                                                                              column=1,
                                                                                                              sticky='w',
                                                                                                              padx=5,
                                                                                                              pady=5)

            Label(profile_data_frame, text="Name              : ", font=('Helvetica', 15), bg='white').grid(row=1,
                                                                                                            column=0,
                                                                                                            sticky='w',
                                                                                                            padx=5,
                                                                                                            pady=5)
            name_entry = Entry(profile_data_frame, font=('Helvetica', 15), width=15)
            name_entry.grid(row=1, column=1, padx=5, pady=5)
            name_entry.insert(0, patient_info['name'])

            Label(profile_data_frame, text="Gender           : ", font=('Helvetica', 15), bg='white').grid(row=2,
                                                                                                           column=0,
                                                                                                           sticky='w',
                                                                                                           padx=5,
                                                                                                           pady=5)
            Label(profile_data_frame, text=patient_info['gender'], font=('Helvetica', 15), bg='white').grid(row=2,
                                                                                                            column=1,
                                                                                                            sticky='w',
                                                                                                            padx=5,
                                                                                                            pady=5)

            Label(profile_data_frame, text="Blood Type     : ", font=('Helvetica', 15), bg='white').grid(row=3,
                                                                                                         column=0,
                                                                                                         sticky='w',
                                                                                                         padx=5,
                                                                                                         pady=5)
            Label(profile_data_frame, text=patient_info['bloodType'], font=('Helvetica', 15), bg='white').grid(row=3,
                                                                                                               column=1,
                                                                                                               sticky='w',
                                                                                                               padx=5,
                                                                                                               pady=5)

            # Age Label and Value
            Label(profile_data_frame, text="Age                : ", font=('Helvetica', 15), bg='white').grid(row=4,
                                                                                                             column=0,
                                                                                                             sticky='w',
                                                                                                             padx=5,
                                                                                                             pady=5)
            Label(profile_data_frame, text=patient_info['age'], font=('Helvetica', 15), bg='white').grid(row=4,
                                                                                                         column=1,
                                                                                                         sticky='w',
                                                                                                         padx=5,
                                                                                                         pady=5)

            # Date of Birth Labels and Values
            Label(profile_data_frame, text="Date of Birth   : ", font=('Helvetica', 15), bg='white').grid(row=5,
                                                                                                          column=0,
                                                                                                          sticky='w',
                                                                                                          padx=5,
                                                                                                          pady=5)

            birth_date_str = f"{patient_info['year']} / {patient_info['month']} / {patient_info['day']}"
            Label(profile_data_frame, text=birth_date_str, font=('Helvetica', 15), bg='white').grid(row=5,
                                                                                                    column=1,
                                                                                                    sticky='w',
                                                                                                    padx=5,
                                                                                                    pady=5)

            # Entry fields for editable fields
            Label(profile_data_frame, text="Password       : ", font=('Helvetica', 15), bg='white').grid(row=6,
                                                                                                         column=0,
                                                                                                         sticky='w',
                                                                                                         padx=5,
                                                                                                         pady=5)
            password_entry = Entry(profile_data_frame, font=('Helvetica', 15), width=15)
            password_entry.grid(row=6, column=1, padx=5, pady=5)
            password_entry.insert(0, patient_info['password'])

            def update_profile():
                new_name = name_entry.get()
                new_password = password_entry.get()

                # Update the profile data
                updated_data = {
                    'name': new_name,
                    'password': new_password
                }

                # Update the profile in Firebase
                try:
                    db.collection('user').document(username).update(updated_data)
                    messagebox.showinfo("Update", "Profile updated successfully")
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {e}")

            update_button = Button(profile_frame, text="Update Profile", command=update_profile, font=('Helvetica', 12))
            update_button.pack(pady=20)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def contact_us():
        clear_content()

        contact_heading = Label(content_area, text="Contact Us", font=('Helvetica', 25, 'bold'), bg='white')
        contact_heading.pack(pady=20)

        contact_frame = Frame(content_area, bg="white", padx=20, pady=20)
        contact_frame.pack()

        # Labels and Entries for Name, Email, and Message
        Label(contact_frame, text="Name          : ", font=('Helvetica', 12), bg='white').grid(row=0, column=0, padx=10,
                                                                                               pady=10)
        name_entry = Entry(contact_frame, font=('Helvetica', 12), width=30)
        name_entry.grid(row=0, column=1, padx=10, pady=10)

        Label(contact_frame, text="Email          : ", font=('Helvetica', 12), bg='white').grid(row=1, column=0,
                                                                                                padx=10, pady=10)
        email_entry = Entry(contact_frame, font=('Helvetica', 12), width=30)
        email_entry.grid(row=1, column=1, padx=10, pady=10)

        Label(contact_frame, text="Message   : ", font=('Helvetica', 12), bg='white').grid(row=2, column=0, padx=10,
                                                                                           pady=10)
        message_entry = Text(contact_frame, font=('Helvetica', 12), width=50, height=10)
        message_entry.grid(row=2, column=1, padx=10, pady=10)

        # Submit Button Functionality
        def submit_message():
            name = name_entry.get()
            email = email_entry.get()
            message = message_entry.get("1.0", "end").strip()

            # Here you can implement further actions like sending an email or saving to database
            messagebox.showinfo("Contact Us", "Message Submitted Successfully")

        submit_button = Button(contact_frame, text="Submit", command=submit_message, font=('Helvetica', 12))
        submit_button.grid(row=3, columnspan=2, pady=20)

    def log_out():
        # Clear the content area
        home_page.destroy()
        run_script1('login_page.py')

    # Create the header frame
    header_frame = Frame(home_page, bg='#07497d', height=100)
    header_frame.pack(fill=X)
    header_label = Label(header_frame, text="Call A Doctor", font=('Helvetica', 35, 'bold'), bg='#07497d',
                         fg='white')
    header_label.pack(side=LEFT, padx=20)
    contact_label = Label(header_frame, text="Contact Us: +1 234 567 890 | email@example.com",
                          font=('Helvetica', 15),
                          bg='#07497d', fg='white')
    contact_label.pack(side=RIGHT, padx=20)

    # Create a Frame for the sidebar
    sidebar = Frame(home_page, width=200, bg='#ADD8E6')
    sidebar.pack(fill=Y, side=LEFT)

    # Load and display the logo
    logo_image = PhotoImage(file="cad1.png")
    logo_label = Label(sidebar, image=logo_image, bg="#ADD8E6")
    logo_label.pack(pady=10, padx=10)
    logo_label.bind("<Button-1>", open_home)

    # Define button events
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

    # Main content area
    content_area = Frame(home_page, bg="white", padx=20, pady=20)
    content_area.pack(expand=True, fill="both")

    # Create buttons for navigation
    create_button("Home", open_home)
    create_button("Profile", open_profile)
    create_button("Book Appointment", book_appointment)
    create_button("Manage Appointment",
                  lambda: messagebox.showinfo("Info", "Manage Appointment feature is under development."))
    # Placeholder for manage appointment
    create_button("Log Out", log_out)

    def clear_content():
        # Clear the content area
        for widget in content_area.winfo_children():
            widget.destroy()

    open_home()

    # Run the main event loop
    home_page.mainloop()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python home_page.py <username>")
    else:
        username = sys.argv[1]
        initialize_home_page(username)
