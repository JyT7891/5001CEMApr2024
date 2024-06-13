import sys
from tkinter import *
from tkinter.ttk import Treeview
from fire_base import initializeFirebase, getClient
from run_script import run_script1


def initialize_home_page(username):
    # Initialize the main window
    home_page = Tk()
    home_page.minsize(1000, 790)
    home_page.resizable(False, False)
    home_page.title(f"Call A Doctor - {username}")

    # Initialize the Firebase Admin SDK
    conn = initializeFirebase()
    db = getClient()

    # Define button events
    def on_enter(event):
        event.widget.config(width=19, height=2, font=('Helvetica', 12, 'bold'))

    def on_leave(event):
        event.widget.config(width=20, height=2, font=('Helvetica', 10))

    def on_click(event):
        event.widget.config(bg="blue")

    def on_release(event):
        event.widget.config(bg="SystemButtonFace")

    # Define button command functions
    def open_home(event=None):
        # Clear the content area
        for widget in content_area.winfo_children():
            widget.destroy()

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

    def search_clinic():
        # Clear the content area
        for widget in content_area.winfo_children():
            widget.destroy()

        # Display the search clinic content
        test = Label(content_area, text="Search Clinic")
        test.pack()

    def book_appointment():
        # Clear the content area
        for widget in content_area.winfo_children():
            widget.destroy()

        # Display the book appointment content
        test = Label(content_area, text="Book Appointment")
        test.pack()

    def manage_appointment():
        # Clear the content area
        for widget in content_area.winfo_children():
            widget.destroy()

        # Display the manage appointment content
        test = Label(content_area, text="Manage Appointment")
        test.pack()

        run_script1("clinic_web.py")

    def open_profile():
        # Clear the content area
        for widget in content_area.winfo_children():
            widget.destroy()

        # Display the profile content
        test = Label(content_area, text="Profile")
        test.pack()

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
    create_button("Search for Clinic", search_clinic)
    create_button("Book Appointment", book_appointment)
    create_button("Manage Appointment", manage_appointment)
    create_button("Profile", open_profile)
    create_button("Log Out", log_out)

    open_home()

    # Run the main event loop
    home_page.mainloop()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python home_page.py <username>")
    else:
        username = sys.argv[1]
        initialize_home_page(username)
