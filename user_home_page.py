import sys
from tkinter import messagebox, PhotoImage, Label, Frame, Entry, Button, Canvas, Scrollbar, LEFT, Y, BOTH, RIGHT, TOP, X
from tkinter import Tk
from tkinter.ttk import Treeview
from PIL import Image, ImageTk
from fire_base import initializeFirebase, getClient  # Assuming these are your Firebase initialization functions
from run_script import run_script1  # Assuming this is your function to run a script
import time


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
        about_frame.grid(row=0, column=0, sticky='nsew')
        about_us_frame(about_frame)

        # Load images carousel on the right side
        carousel_frame = Frame(content_frame, bg="white", width=700, height=400)
        carousel_frame.grid(row=0, column=1, padx=20, pady=10, sticky='nsew')
        load_images(carousel_frame)

    def load_images(slide_show_frame):
        image_files = ["carousel1.jpg", "carousel2.jpg", "carousel3.jpg"]  # Replace with your image filenames

        images = []
        for img_file in image_files:
            try:
                image = Image.open(img_file)
                resized_image = image.resize((700, 400))
                photo_image = ImageTk.PhotoImage(resized_image)
                images.append(photo_image)
            except IOError as e:
                print(f"Error loading image {img_file}: {e}")

        current_image_label = Label(slide_show_frame, bg="white")
        next_image_label = Label(slide_show_frame, bg="white")
        current_image_label.pack()
        next_image_label.pack()

        idx = 0
        transition_duration = 2000  # Transition duration in milliseconds

        def update_image():
            nonlocal idx
            current_image = images[idx]
            next_image = images[(idx + 1) % len(images)]

            current_image_label.config(image=current_image)
            current_image_label.place(relwidth=1, relheight=1)
            current_image_label.lift()

            next_image_label.config(image=next_image)
            next_image_label.place(relwidth=1, relheight=1)
            next_image_label.lift()

            for alpha in range(0, 101, 5):  # Fade out current image
                current_image_label.place(relwidth=1, relheight=1)
                current_image_label.lift()

                next_image_label.place(relwidth=1, relheight=1)
                next_image_label.lift()

                slide_show_frame.update()
                time.sleep(transition_duration / 1000 / 20)

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
        clear_content()
        profile_frame = Frame(content_area, background='white')
        profile_frame.pack(padx=50, pady=20)
        profile_label = Label(profile_frame, text="Profile", font=('Helvetica', 30, 'bold'), background='white',
                              fg='#07497d')
        profile_label.pack()
        try:
            doc = db.collection('user').document(username).get()
            if doc.exists:
                patient_info = doc.to_dict()
            else:
                patient_info = {'username': 'N/A', 'age': 'N/A', 'email': 'N/A', 'password': 'N/A', 'blood_type': 'N/A'}
            profile_data_frame = Frame(profile_frame, background='white')
            profile_data_frame.pack(padx=20, pady=20)
            Label(profile_data_frame, text="Username       : ", font=('Helvetica', 15), bg='white', fg='#07497d').grid(
                row=0, column=0, sticky='w', padx=5, pady=5)
            Label(profile_data_frame, text=patient_info['username'], font=('Helvetica', 15), bg='white',
                  fg='#07497d').grid(row=0, column=1, sticky='w', padx=5, pady=5)
            Label(profile_data_frame, text="Name              : ", font=('Helvetica', 15), bg='white',
                  fg='#07497d').grid(row=1, column=0, sticky='w', padx=5, pady=5)
            name_entry = Entry(profile_data_frame, font=('Helvetica', 15), width=15)
            name_entry.grid(row=1, column=1, padx=5, pady=5)
            name_entry.insert(0, patient_info['name'])
            Label(profile_data_frame, text="Blood Type    : ", font=('Helvetica', 15), bg='white', fg='#07497d').grid(
                row=3, column=0, sticky='w', padx=5, pady=5)
            Label(profile_data_frame, text=patient_info['blood_type'], font=('Helvetica', 15), bg='white',
                  fg='#07497d').grid(row=3, column=1, sticky='w', padx=5, pady=5)
            Label(profile_data_frame, text="Age                : ", font=('Helvetica', 15), bg='white',
                  fg='#07497d').grid(row=4, column=0, sticky='w', padx=5, pady=5)
            Label(profile_data_frame, text=patient_info['age'], font=('Helvetica', 15), bg='white', fg='#07497d').grid(
                row=4, column=1, sticky='w', padx=5, pady=5)
            Label(profile_data_frame, text="Email              : ", font=('Helvetica', 15), bg='white',
                  fg='#07497d').grid(row=5, column=0, sticky='w', padx=5, pady=5)
            email_entry = Entry(profile_data_frame, font=('Helvetica', 15), width=15)
            email_entry.grid(row=5, column=1, padx=5, pady=5)
            email_entry.insert(0, patient_info['email'])
            Label(profile_data_frame, text="Password        : ", font=('Helvetica', 15), bg='white', fg='#07497d').grid(
                row=6, column=0, sticky='w', padx=5, pady=5)
            password_entry = Entry(profile_data_frame, font=('Helvetica', 15), width=15, show="*")
            password_entry.grid(row=6, column=1, padx=5, pady=5)
            password_entry.insert(0, patient_info['password'])
            update_button = Button(profile_data_frame, text="Update", font=('Helvetica', 15), bg='#07497d', fg='white',
                                   command=lambda: update_profile(name_entry.get(), email_entry.get(),
                                                                  password_entry.get()))
            update_button.grid(row=7, columnspan=2, pady=10)
        except Exception as e:
            print(f"An error occurred: {e}")

    def update_profile(name, email, password):
        try:
            user_ref = db.collection('user').document(username)
            user_ref.update({
                'name': name,
                'email': email,
                'password': password
            })
            messagebox.showinfo("Update", "Profile updated successfully.")
        except Exception as e:
            messagebox.showerror("Update Failed", f"An error occurred while updating profile: {e}")

    def clear_content():
        for widget in content_area.winfo_children():
            widget.destroy()

    # Create the header frame
    header_frame = Frame(home_page, bg='#07497d', height=100)
    header_frame.pack(fill=X)
    header_label = Label(header_frame, text="Call A Doctor", font=('Helvetica', 35, 'bold'), bg='#07497d', fg='white')
    header_label.pack(side=LEFT, padx=20)
    contact_label = Label(header_frame, text="Contact Us: +1 234 567 890 | email@example.com", font=('Helvetica', 15),
                          bg='#07497d', fg='white')
    contact_label.pack(side=RIGHT, padx=20)

    # Create the sidebar frame
    sidebar_frame = Frame(home_page, bg='#ADD8E6', width=200)
    sidebar_frame.pack(side=LEFT, fill=Y)
    sidebar_label = Label(sidebar_frame, text="Navigation", font=('Helvetica', 20, 'bold'), bg='#ADD8E6', fg='#07497d')
    sidebar_label.pack(pady=10)

    buttons = [
        ("Home", open_home),
        ("Profile", open_profile),
        ("Book Appointment", book_appointment),
        ("Manage Appointment", lambda: messagebox.showinfo("Info", "Manage Appointment feature is under development.")),
        # Placeholder for manage appointment
        ("Log Out", home_page.quit)
    ]
    for text, command in buttons:
        button = Button(sidebar_frame, text=text, font=('Helvetica', 15), bg='#ADD8E6', fg='#07497d', command=command)
        button.pack(fill=X, pady=5, padx=10)

    # Create the main content area
    content_area = Frame(home_page, bg='white')
    content_area.pack(fill=BOTH, expand=True)

    # Initialize with home content
    open_home()

    # Run the main event loop
    home_page.mainloop()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python home_page.py <username>")
    else:
        username = sys.argv[1]
        initialize_home_page(username)
