import sys
from tkinter import messagebox
from tkinter import *
from tkinter.ttk import Treeview, Style
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

    # Define button command functions
    def open_home(event=None):
        # Clear the content area
        clear_content()

        # Display the home page content
        welcome = Label(content_area, text="Welcome to Call A Doctor - Your Partner in Health", background='white',
                        font=('Helvetica', 25, 'bold'))
        welcome.pack()
        about_us_frame()
        patient_information(username)

    def patient_information(username):
        patient_frame = Frame(content_area, background='white')
        patient_frame.pack(padx=50, pady=20)

        # Fetch patient data from the database
        try:
            doc = db.collection('user').document(username).get()
            if doc.exists:
                patient_info = doc.to_dict()
            else:
                patient_info = {'username': 'N/A', 'age': 'N/A', 'email': 'N/A', 'blood_type': 'N/A'}

            patient_profile = Label(patient_frame, text="Profile", font=('Helvetica', 30, 'bold'), background='white')
            patient_profile.pack()

            # Display patient profile information in a table
            tree = Treeview(patient_frame, columns=("Attribute", "Value"), show='headings', height=4)
            tree.pack(side='left')

            tree.heading("Attribute", text="Attribute")
            tree.heading("Value", text="Value")

            # Define the order of attributes to display
            attribute_order = ["username", "age", "email", "bloodType"]

            # Insert patient data into the table based on the specified order
            for attribute in attribute_order:
                value = patient_info.get(attribute, 'N/A')
                tree.insert('', 'end', values=(attribute.capitalize(), value))

        except Exception as e:
            print(f"An error occurred: {e}")

    def about_us_frame():
        about_frame = Frame(content_area)
        about_frame.pack(padx=50, pady=20)

        about_text = """
            Welcome to Call A Doctor!

            Call A Doctor is committed to providing high-quality healthcare services to our patients. 
            Whether you need to search for clinics, book appointments, or manage your appointments, 
            our platform is here to assist you every step of the way.

            Our dedicated team works tirelessly to ensure that you receive the best possible care. 
            Thank you for choosing Call A Doctor as your partner in health!

            For any inquiries or assistance, please feel free to contact us.
            """

        about_label = Label(about_frame, text=about_text, justify=LEFT, background='#ADD8E6', font=('Helvetica', 15))
        about_label.pack()

    def fetch_clinics_from_firebase():
        clinics_ref = db.collection('clinic')
        docs = clinics_ref.stream()
        clinics = []
        for doc in docs:
            clinic = doc.to_dict()
            clinics.append(clinic)
        return clinics

    def book_appointment():
        # Clear the content area
        clear_content()

        # Display the book appointment content
        text = Label(content_area, text="Book Appointment", font=('Helvetica', 25, 'bold'), background="white")
        text.pack(pady=10)

        # Fetch clinics from Firebase
        clinics = fetch_clinics_from_firebase()

        def button_command():
            home_page.withdraw()
            run_script1('show_map.py')

        # Create a canvas and a scrollbar
        canvas = Canvas(content_area, bg="white")
        scrollbar = Scrollbar(content_area, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas, bg="white")

        # Configure the scrollable frame
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack the canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Fixed width for each clinic frame
        frame_width = 300
        frame_height = 150

        # Calculate the number of columns
        num_columns = 3

        # Display each clinic in its own styled frame
        for idx, clinic in enumerate(clinics):
            row = idx // num_columns
            column = idx % num_columns

            clinic_frame = Frame(scrollable_frame, bd=0, relief="groove", padx=10, pady=10, bg="#f0f0f0",
                                 width=frame_width, height=frame_height)
            clinic_frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

            clinic_name_label = Label(clinic_frame, text=clinic['name'], font=('Helvetica', 15, 'bold'), bg="#f0f0f0")
            clinic_name_label.pack(anchor="w")

            clinic_num_label = Label(clinic_frame, text=clinic['phone_num'], font=('Helvetica', 12), bg="#f0f0f0")
            clinic_num_label.pack(anchor="w")

            open_time_label = Label(clinic_frame, text=f"Open Time: {clinic['open_time']}", font=('Helvetica', 12),
                                    bg="#f0f0f0")
            open_time_label.pack(anchor="w", pady=2)

            close_time_label = Label(clinic_frame, text=f"Close Time: {clinic['close_time']}", font=('Helvetica', 12),
                                     bg="#f0f0f0")
            close_time_label.pack(anchor="w", pady=2)

            # Bind the click event to the clinic frame
            clinic_frame.bind("<Button-1>",
                              lambda event, clinic_name=clinic['name']: button_command())

            # Make the frame's width and height fixed
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
            Label(profile_data_frame, text="Username       : ", font=('Helvetica', 15), bg='white').grid(row=0, column=0,
                                                                                                      sticky='w',
                                                                                                      padx=5,
                                                                                                      pady=5)
            Label(profile_data_frame, text=patient_info['username'], font=('Helvetica', 15), bg='white').grid(row=0,
                                                                                                              column=1,
                                                                                                              sticky='w',
                                                                                                              padx=5,
                                                                                                              pady=5)

            Label(profile_data_frame, text="Gender           : ", font=('Helvetica', 15), bg='white').grid(row=1, column=0,
                                                                                                        sticky='w',
                                                                                                        padx=5,
                                                                                                        pady=5)
            Label(profile_data_frame, text=patient_info['gender'], font=('Helvetica', 15), bg='white').grid(row=1,
                                                                                                            column=1,
                                                                                                            sticky='w',
                                                                                                            padx=5,
                                                                                                            pady=5)

            Label(profile_data_frame, text="Blood Type     : ", font=('Helvetica', 15), bg='white').grid(row=2, column=0,
                                                                                                      sticky='w',
                                                                                                      padx=5,
                                                                                                      pady=5)
            Label(profile_data_frame, text=patient_info['bloodType'], font=('Helvetica', 15), bg='white').grid(row=2,
                                                                                                               column=1,
                                                                                                               sticky='w',
                                                                                                               padx=5,
                                                                                                               pady=5)

            # Age Label and Value
            Label(profile_data_frame, text="Age                : ", font=('Helvetica', 15), bg='white').grid(row=3,
                                                                                                          column=0,
                                                                                                          sticky='w',
                                                                                                          padx=5,
                                                                                                          pady=5)
            Label(profile_data_frame, text=patient_info['age'], font=('Helvetica', 15), bg='white').grid(row=3,
                                                                                                         column=1,
                                                                                                         sticky='w',
                                                                                                         padx=5,
                                                                                                         pady=5)

            # Date of Birth Labels and Values
            Label(profile_data_frame, text="Date of Birth   : ", font=('Helvetica', 15), bg='white').grid(row=4,
                                                                                                          column=0,
                                                                                                          sticky='w',
                                                                                                          padx=5,
                                                                                                          pady=5)

            birth_date_str = f"{patient_info['year']} / {patient_info['month']} / {patient_info['day']}"
            Label(profile_data_frame, text=birth_date_str, font=('Helvetica', 15), bg='white').grid(row=4,
                                                                                                    column=1,
                                                                                                    sticky='w',
                                                                                                    padx=5,
                                                                                                    pady=5)

            # Entry fields for editable fields
            Label(profile_data_frame, text="Email              : ", font=('Helvetica', 15), bg='white').grid(row=5,
                                                                                                          column=0,
                                                                                                          sticky='w',
                                                                                                          padx=5,
                                                                                                          pady=5)
            email_entry = Entry(profile_data_frame, font=('Helvetica', 15), width=15)
            email_entry.grid(row=5, column=1, padx=5, pady=5)
            email_entry.insert(0, patient_info['email'])

            Label(profile_data_frame, text="Password       : ", font=('Helvetica', 15), bg='white').grid(row=6, column=0,
                                                                                                      sticky='w',
                                                                                                      padx=5,
                                                                                                      pady=5)
            password_entry = Entry(profile_data_frame, font=('Helvetica', 15), width=15)
            password_entry.grid(row=6, column=1, padx=5, pady=5)
            password_entry.insert(0, patient_info['password'])

            def update_profile():
                new_email = email_entry.get()
                new_password = password_entry.get()

                # Update the profile data
                updated_data = {
                    'email': new_email,
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

    # Create a Frame for the sidebar
    sidebar = Frame(home_page, width=200, bg="lavender")
    sidebar.pack(fill=Y, side=LEFT)

    # Load and display the logo
    logo_image = PhotoImage(file="cad1.png")
    logo_label = Label(sidebar, image=logo_image, bg="lavender")
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
    create_button("Book Appointment", book_appointment)
    create_button("Profile", open_profile)
    create_button("Contact Us", contact_us)
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
