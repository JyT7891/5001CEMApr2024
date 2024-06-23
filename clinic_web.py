import calendar
from datetime import datetime, date
from tkinter import *
from tkinter import messagebox, ttk
from tkinter.ttk import Combobox

from fire_base import initializeFirebase, getClient
from run_script import run_script1

admin_clinic = Tk()
admin_clinic.minsize(1300, 790)
admin_clinic.resizable(False, False)
admin_clinic.title("Call A Doctor Admin Page ")

# Create the header frame
header_frame = Frame(admin_clinic, bg='#07497d', height=100)
header_frame.pack(fill=X)
header_label = Label(header_frame, text="Call A Doctor", font=('Helvetica', 35, 'bold'), bg='#07497d', fg='white')
header_label.pack(side=LEFT, padx=20)
contact_label = Label(header_frame, text="Contact Us: +1 234 567 890 | email@example.com", font=('Helvetica', 15),
                      bg='#07497d', fg='white')
contact_label.pack(side=RIGHT, padx=20)

def create_grid_list(parent, items, item_type):
    global add_button_command, add_button_text
    clear_content()

    # Header Frame
    header_frame = Frame(parent)
    header_frame.pack(fill='x', padx=20, pady=10)

    # Add Button in the Header Frame
    if item_type == 'clinic':
        add_button_text = "Add Clinic"
        add_button_command = add_clinic
    elif item_type == 'doctor':
        add_button_text = "Add Doctor"
        add_button_command = add_doctor
    elif item_type == 'user':
        add_button_text = "Add User"
        add_button_command = add_user

    add_button = Button(header_frame, text=add_button_text, font=('Helvetica', 15), fg='white', bg='#07497d',
                        command=add_button_command)
    add_button.pack(side="top", padx=10, pady=5)

    # Scrollable Frame
    scrollable_frame = ttk.Frame(parent)
    scrollable_frame.pack(expand=True, fill='both')

    canvas = Canvas(scrollable_frame)
    scrollbar = Scrollbar(scrollable_frame, orient="vertical", command=canvas.yview)
    scroll_frame = Frame(canvas)

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Define grid parameters
    frame_width = 300
    frame_height = 200
    num_columns = 3

    # Create items in the grid list
    for idx, item in enumerate(items):
        row = idx // num_columns * 2 + 1
        column = idx % num_columns

        item_frame = Frame(scroll_frame, bd=1, relief="solid", padx=10, pady=10, bg="#f0f0f0", width=frame_width,
                           height=frame_height)
        item_frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

        if item_type == 'clinic':
            item_label = Label(item_frame, text=item['name'], font=('Helvetica', 15, 'bold'), bg="#f0f0f0",
                               fg='#07497d')
            item_label.pack(anchor="w")
            item_detail_label = Label(item_frame, text=item['phone_num'], font=('Helvetica', 12), bg="#f0f0f0",
                                      fg='#07497d')
            item_detail_label.pack(anchor="w")
            open_time_label = Label(item_frame, text=f"Open Time: {item['open_time']}", font=('Helvetica', 12),
                                    bg="#f0f0f0", fg='#07497d')
            open_time_label.pack(anchor="w", pady=2)
            close_time_label = Label(item_frame, text=f"Close Time: {item['close_time']}", font=('Helvetica', 12),
                                     bg="#f0f0f0", fg='#07497d')
            close_time_label.pack(anchor="w", pady=2)

            # Edit button for clinics
            edit_button = Button(item_frame, text="Edit", bg="green", fg="white", width=10, height=1,
                                 font=('Helvetica', 12), command=lambda cid=item['clinic_id']: edit_clinic(cid))
            edit_button.pack(side="right", padx=5, pady=5)

            # Delete button for clinics
            delete_button = Button(item_frame, text="Delete", bg="red", fg="white", width=10, height=1,
                                   font=('Helvetica', 12), command=lambda cid=item['clinic_id']: delete_clinic(cid))
            delete_button.pack(side="left", padx=5, pady=5)

        elif item_type == 'doctor':
            item_label = Label(item_frame, text=item['doc_name'], font=('Helvetica', 15, 'bold'), bg="#f0f0f0",
                               fg='#07497d')
            item_label.pack(anchor="w")
            item_detail_label = Label(item_frame, text=item['service'], font=('Helvetica', 12), bg="#f0f0f0",
                                      fg='#07497d')
            item_detail_label.pack(anchor="w")
            clinic_name = get_clinic_name(item['clinic_id'])  # Fetch clinic name based on clinic_id
            clinic_label = Label(item_frame, text=f"Clinic: {clinic_name}", font=('Helvetica', 12), bg="#f0f0f0",
                                 fg='#07497d')
            clinic_label.pack(anchor="w", pady=2)
            availability_label = Label(item_frame, text=f"Available: {item['is_Available']}", font=('Helvetica', 12),
                                       bg="#f0f0f0", fg='#07497d')
            availability_label.pack(anchor="w", pady=2)

            # Edit button for doctors
            edit_button = Button(item_frame, text="Edit", bg="green", fg="white", width=10, height=1,
                                 font=('Helvetica', 12), command=lambda did=item['doctor_id']: edit_doctor(did))
            edit_button.pack(side="right", padx=5, pady=5)

            # Delete button for doctors
            delete_button = Button(item_frame, text="Delete", bg="red", fg="white", width=10, height=1,
                                   font=('Helvetica', 12), command=lambda did=item['doctor_id']: delete_doctor(did))
            delete_button.pack(side="left", padx=5, pady=5)

        elif item_type == 'user':
            item_label = Label(item_frame, text=item['name'], font=('Helvetica', 15, 'bold'), bg="#f0f0f0",
                               fg='#07497d')
            item_label.pack(anchor="w")
            item_detail_label = Label(item_frame, text=f"Gender        :  {item['gender']}", font=('Helvetica', 12),
                                      bg="#f0f0f0", fg='#07497d')
            item_detail_label.pack(anchor="w")
            blood_type_label = Label(item_frame, text=f"Blood Type :  {item['bloodType']}", font=('Helvetica', 12),
                                     bg="#f0f0f0", fg='#07497d')
            blood_type_label.pack(anchor="w", pady=2)
            age_label = Label(item_frame, text=f"Age              :  {item['age']}", font=('Helvetica', 12),
                              bg="#f0f0f0", fg='#07497d')
            age_label.pack(anchor="w", pady=2)

            # Edit button for users
            edit_button = Button(item_frame, text="Edit", bg="green", fg="white", width=10, height=1,
                                 font=('Helvetica', 12), command=lambda uid=item['username']: edit_user(uid))
            edit_button.pack(side="right", padx=5, pady=5)

            # Delete button for users
            delete_button = Button(item_frame, text="Delete", bg="red", fg="white", width=10, height=1,
                                   font=('Helvetica', 12), command=lambda uid=item['name']: delete_user(uid))
            delete_button.pack(side="left", padx=5, pady=5)

        item_frame.pack_propagate(False)


def get_clinics(db):
    clinics_ref = db.collection('clinic')
    clinics = []
    for clinic in clinics_ref.stream():
        clinics.append(clinic.to_dict())
    return clinics


def get_doctors(db):
    doctors_ref = db.collection('doctor')
    doctors = []
    for doctor in doctors_ref.stream():
        doctors.append(doctor.to_dict())
    return doctors


def get_users(db):
    users_ref = db.collection('user')
    users = []
    for user in users_ref.stream():
        users.append(user.to_dict())
    return users

# Function to get clinic name based on clinic_id
def get_clinic_name(clinic_id):
    clinic_ref = db.collection('clinic').document(clinic_id)
    clinic = clinic_ref.get()
    if clinic.exists:
        return clinic.to_dict()['name']
    else:
        return "Unknown Clinic"

def clinic_list():
    clinics = get_clinics(db)
    create_grid_list(content_area, clinics, 'clinic')


def doctor_list():
    doctors = get_doctors(db)
    create_grid_list(content_area, doctors, 'doctor')


def user_list():
    users = get_users(db)
    create_grid_list(content_area, users, 'user')


def log_out():
    admin_clinic.destroy()
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
    button.pack(fill='x', padx=20, pady=10)
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)


# Clinic
def add_clinic():
    def get_clinic_count():
        # Function to get the current count of clinics in Firestore
        clinics_ref = db.collection('clinic')
        return len(list(clinics_ref.get()))

    clinic_id = f"Clinic{get_clinic_count() + 1}"  # Generate unique clinic name

    # Function to add a new clinic to Firebase
    def submit_clinic():
        new_clinic = {
            'clinic_id': clinic_id,
            'name': name_entry.get(),
            'phone_num': phone_entry.get(),
            'open_time': open_time_entry.get(),
            'close_time': close_time_entry.get()
            # Add more fields as needed
        }
        # Add new clinic to Firebase collection
        db.collection('clinic').document(clinic_id).set(new_clinic)
        messagebox.showinfo("Success", "New clinic added successfully")
        # Clear the form entries after submission
        name_entry.delete(0, END)
        phone_entry.delete(0, END)
        open_time_entry.delete(0, END)
        close_time_entry.delete(0, END)
        # Update clinic list display
        clinic_list()
        add_clinic_window.destroy()

    # Create a Toplevel window for adding clinic
    add_clinic_window = Toplevel(admin_clinic)
    add_clinic_window.title("Add New Clinic")
    add_clinic_window.minsize(500, 300)
    add_clinic_window.resizable(False, False)

    # Clinic Name
    Label(add_clinic_window, text="Clinic Name    : ", font=('Helvetica', 12)).grid(row=0, column=0, padx=10, pady=5,
                                                                                    sticky="e")
    name_entry = Entry(add_clinic_window, width=25, font='Arial 19')
    name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    # Phone Number
    Label(add_clinic_window, text="Phone Number    : ", font=('Helvetica', 12)).grid(row=1, column=0, padx=10, pady=5,
                                                                                     sticky="e")
    phone_entry = Entry(add_clinic_window, width=25, font='Arial 19')
    phone_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    # Open Time
    Label(add_clinic_window, text="Open Time      : ", font=('Helvetica', 12)).grid(row=2, column=0, padx=10, pady=5,
                                                                                    sticky="e")
    open_time_entry = Entry(add_clinic_window, width=25, font='Arial 19')
    open_time_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    # Close Time
    Label(add_clinic_window, text="Close Time      : ", font=('Helvetica', 12)).grid(row=3, column=0, padx=10, pady=5,
                                                                                     sticky="e")
    close_time_entry = Entry(add_clinic_window, width=25, font='Arial 19')
    close_time_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    # Submit Button
    submit_button = Button(add_clinic_window, text="Submit", command=submit_clinic, height=1, width=10,
                           font=('Arial', 20))
    submit_button.grid(row=4, columnspan=2, padx=10, pady=10, ipadx=50)

    add_clinic_window.mainloop()


def delete_clinic(clinic_id):
    confirmed = messagebox.askyesno("Confirmation", "Are you sure you want to delete this clinic?")
    if confirmed:
        db.collection('clinic').document(clinic_id).delete()
        messagebox.showinfo("Success", "Clinic deleted successfully")
        clinic_list()
    else:
        messagebox.showinfo("Cancelled", "Deletion cancelled by user")


def edit_clinic(clinic_id):
    def update_clinic():
        updated_clinic = {
            'name': name_entry.get(),
            'phone_num': phone_entry.get(),
            'open_time': open_time_entry.get(),
            'close_time': close_time_entry.get()
            # Add more fields as needed
        }
        # Update clinic in Firestore
        db.collection('clinic').document(clinic_id).update(updated_clinic)
        messagebox.showinfo("Success", "Clinic updated successfully")
        # Clear form entries after update
        name_entry.delete(0, END)
        phone_entry.delete(0, END)
        open_time_entry.delete(0, END)
        close_time_entry.delete(0, END)
        # Update clinic list display
        clinic_list()
        edit_clinic_window.destroy()

    # Fetch current clinic details
    clinic_ref = db.collection('clinic').document(clinic_id)
    clinic_data = clinic_ref.get().to_dict()

    # Create a Toplevel window for editing clinic
    edit_clinic_window = Toplevel(admin_clinic)
    edit_clinic_window.title("Edit Clinic")
    edit_clinic_window.minsize(500, 300)
    edit_clinic_window.resizable(False, False)

    # Clinic Name
    Label(edit_clinic_window, text="Clinic Name    : ", font=('Helvetica', 12)).grid(row=0, column=0, padx=10, pady=5,
                                                                                     sticky="e")
    name_entry = Entry(edit_clinic_window, width=25, font='Arial 19')
    name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")
    name_entry.insert(0, clinic_data['name'])

    # Phone Number
    Label(edit_clinic_window, text="Phone Number    : ", font=('Helvetica', 12)).grid(row=1, column=0, padx=10, pady=5,
                                                                                      sticky="e")
    phone_entry = Entry(edit_clinic_window, width=25, font='Arial 19')
    phone_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
    phone_entry.insert(0, clinic_data['phone_num'])

    # Open Time
    Label(edit_clinic_window, text="Open Time      : ", font=('Helvetica', 12)).grid(row=2, column=0, padx=10, pady=5,
                                                                                     sticky="e")
    open_time_entry = Entry(edit_clinic_window, width=25, font='Arial 19')
    open_time_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
    open_time_entry.insert(0, clinic_data['open_time'])

    # Close Time
    Label(edit_clinic_window, text="Close Time      : ", font=('Helvetica', 12)).grid(row=3, column=0, padx=10, pady=5,
                                                                                      sticky="e")
    close_time_entry = Entry(edit_clinic_window, width=25, font='Arial 19')
    close_time_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")
    close_time_entry.insert(0, clinic_data['close_time'])

    # Submit Button
    submit_button = Button(edit_clinic_window, text="Update", command=update_clinic, height=1, width=10,
                           font=('Arial', 20))
    submit_button.grid(row=4, columnspan=2, padx=10, pady=10, ipadx=50)

    edit_clinic_window.mainloop()


# Doctor
def add_doctor():
    def get_doctor_count():
        # Function to get the current count of doctors in Firestore
        doctors_ref = db.collection('doctor')
        return len(list(doctors_ref.get()))

    def submit_doctor():
        # Fetch clinic ID based on selected clinic name
        selected_clinic_name = clinic_var.get()
        selected_clinic = next((clinic for clinic in clinics if clinic['name'] == selected_clinic_name), None)

        doctor_id = f"doctor{get_doctor_count() + 1}"  # Generate unique doctor name

        if selected_clinic:
            new_doctor = {
                'doc_name': name_entry.get(),
                'service': service_entry.get(),
                'clinic_id': selected_clinic['clinic_id'],
                'is_Available': availability_var.get(),
                'doctor_id': doctor_id,
                'password': doctor_id
            }
            # Add new doctor to Firestore collection
            db.collection('doctor').document(doctor_id).set(new_doctor)
            messagebox.showinfo("Success", "New doctor added successfully")
            # Clear form entries after submission
            name_entry.delete(0, END)
            service_entry.delete(0, END)
            availability_var.set("True")  # Reset dropdown selection
            # Update doctor list display
            doctor_list()
            add_doctor_window.destroy()
        else:
            messagebox.showerror("Error", "Selected clinic not found. Please select a valid clinic.")

    # Fetch clinics from Firestore
    clinics = get_clinics(db)
    clinic_names = [clinic['name'] for clinic in clinics]

    # Create a Toplevel window for adding a doctor
    add_doctor_window = Toplevel(admin_clinic)
    add_doctor_window.title("Add New Doctor")
    add_doctor_window.minsize(500, 300)
    add_doctor_window.resizable(False, False)

    # Doctor Name
    Label(add_doctor_window, text="Doctor Name    : ", font=('Helvetica', 12)).grid(row=0, column=0, padx=10, pady=5,
                                                                                    sticky="e")
    name_entry = Entry(add_doctor_window, width=25, font='Arial 19')
    name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    # Service
    Label(add_doctor_window, text="Service    : ", font=('Helvetica', 12)).grid(row=1, column=0, padx=10, pady=5,
                                                                                sticky="e")
    service_entry = Entry(add_doctor_window, width=25, font='Arial 19')
    service_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    # Clinic Name Dropdown
    Label(add_doctor_window, text="Clinic Name    : ", font=('Helvetica', 12)).grid(row=2, column=0, padx=10, pady=5,
                                                                                    sticky="e")
    clinic_var = StringVar(add_doctor_window)
    clinic_var.set(clinic_names[0])  # Set default value
    clinic_dropdown = OptionMenu(add_doctor_window, clinic_var, *clinic_names)
    clinic_dropdown.config(width=22, font=('Arial', 12))
    clinic_dropdown.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    # Availability
    Label(add_doctor_window, text="Availability    : ", font=('Helvetica', 12)).grid(row=3, column=0, padx=10, pady=5,
                                                                                     sticky="e")
    availability_var = StringVar(add_doctor_window)
    availability_var.set("True")  # Set default value
    availability_dropdown = OptionMenu(add_doctor_window, availability_var, "True", "False")
    availability_dropdown.config(width=22, font=('Arial', 12))
    availability_dropdown.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    # Submit Button
    submit_button = Button(add_doctor_window, text="Submit", command=submit_doctor, height=1, width=10,
                           font=('Arial', 20))
    submit_button.grid(row=4, columnspan=2, padx=10, pady=10, ipadx=50)

    add_doctor_window.mainloop()


def delete_doctor(doctor_id):
    confirmed = messagebox.askyesno("Confirmation", "Are you sure you want to delete this doctor?")
    if confirmed:
        try:
            # Delete doctor from Firebase
            db.collection('doctor').document(doctor_id).delete()
            messagebox.showinfo("Success", "Doctor deleted successfully")
            # Refresh doctor list after deletion
            doctor_list()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    else:
        messagebox.showinfo("Cancelled", "Deletion cancelled by user")


def edit_doctor(doctor_id):
    def update_doctor():
        availability_value = availability_combobox.get()
        is_available = True if availability_value == "Yes" else False

        updated_doctor = {
            'doc_name': name_entry.get(),
            'service': service_entry.get(),
            'clinic_id': clinic_id_entry.get(),
            'is_Available': is_available
            # Add more fields as needed
        }
        db.collection('doctor').document(doctor_id).update(updated_doctor)
        messagebox.showinfo("Success", "Doctor updated successfully")
        name_entry.delete(0, END)
        service_entry.delete(0, END)
        clinic_id_entry.delete(0, END)
        availability_combobox.set('')
        doctor_list()
        edit_doctor_window.destroy()

    doctor_ref = db.collection('doctor').document(doctor_id)
    doctor_data = doctor_ref.get().to_dict()

    edit_doctor_window = Toplevel(admin_clinic)
    edit_doctor_window.title("Edit Doctor")
    edit_doctor_window.minsize(500, 300)
    edit_doctor_window.resizable(False, False)

    Label(edit_doctor_window, text="Doctor Name    : ", font=('Helvetica', 12)).grid(row=0, column=0, padx=10, pady=5,
                                                                                     sticky="e")
    name_entry = Entry(edit_doctor_window, width=25, font='Arial 19')
    name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")
    name_entry.insert(0, doctor_data['doc_name'])

    Label(edit_doctor_window, text="Service Type    : ", font=('Helvetica', 12)).grid(row=1, column=0, padx=10, pady=5,
                                                                                      sticky="e")
    service_entry = Entry(edit_doctor_window, width=25, font='Arial 19')
    service_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
    service_entry.insert(0, doctor_data['service'])

    Label(edit_doctor_window, text="Clinic ID      : ", font=('Helvetica', 12)).grid(row=2, column=0, padx=10, pady=5,
                                                                                     sticky="e")
    clinic_id_entry = Entry(edit_doctor_window, width=25, font='Arial 19')
    clinic_id_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
    clinic_id_entry.insert(0, doctor_data['clinic_id'])

    Label(edit_doctor_window, text="Availability   : ", font=('Helvetica', 12)).grid(row=3, column=0, padx=10, pady=5,
                                                                                     sticky="e")
    availability_combobox = Combobox(edit_doctor_window, values=["Yes", "No"], font='Arial 19', state="readonly")
    availability_combobox.grid(row=3, column=1, padx=10, pady=5, sticky="w")
    availability_combobox.set("Yes" if doctor_data['is_Available'] else "No")

    submit_button = Button(edit_doctor_window, text="Update", command=update_doctor, height=1, width=10,
                           font=('Arial', 20))
    submit_button.grid(row=4, columnspan=2, padx=10, pady=10, ipadx=50)

    edit_doctor_window.mainloop()


def add_user():
    def calculate_age(birthdate):
        # Calculate age based on current year
        current_year = datetime.now().year
        birth_year = birthdate.year
        age = current_year - birth_year
        return age

    def submit_user():
        name = name_entry.get()
        # Get user input data
        new_user = {
            'username': username_entry.get(),
            'name': name,
            'gender': gender_var.get(),
            'bloodType': blood_type_var.get(),
            'year': year_var.get(),
            'month': month_var.get(),
            'day': day_var.get(),
            'age': calculate_age(datetime.strptime(f"{year_var.get()}-{month_var.get()}-{day_var.get()}", '%Y-%m-%d')),
            'password': '1234'
        }

        db.collection('user').document(name).set(new_user)
        messagebox.showinfo("Success", "New user added successfully")
        # Clear form entries after submission
        username_entry.delete(0, END)
        name_entry.delete(0, END)
        year_var.set("")  # Reset year dropdown
        month_var.set("")  # Reset month dropdown
        day_var.set("")  # Reset day dropdown
        gender_var.set("Male")  # Reset gender dropdown
        blood_type_var.set("O")  # Reset blood type dropdown
        # Update user list display after add
        user_list()
        add_user_window.destroy()

    # Create a Toplevel window for adding a user
    add_user_window = Toplevel()
    add_user_window.title("Add New User")
    add_user_window.minsize(500, 300)
    add_user_window.resizable(False, False)

    # Username
    Label(add_user_window, text="Username   :", font=('Helvetica', 12)).place(x=10, y=15)
    username_entry = Entry(add_user_window, width=30, font='Arial 15')
    username_entry.place(x=120, y=10)

    # Name
    Label(add_user_window, text="Name           :", font=('Helvetica', 12)).place(x=10, y=65)
    name_entry = Entry(add_user_window, width=30, font='Arial 15')
    name_entry.place(x=120, y=65)

    # Gender
    Label(add_user_window, text="Gender         :", font=('Helvetica', 12)).place(x=10, y=115)
    gender_var = StringVar(add_user_window)
    gender_var.set("Male")  # Set default value
    gender_dropdown = OptionMenu(add_user_window, gender_var, "Male", "Female", "Other")
    gender_dropdown.config(width=20, font=('Arial', 12))
    gender_dropdown.place(x=120, y=110)

    # Blood Type
    Label(add_user_window, text="Blood Type   :", font=('Helvetica', 12)).place(x=10, y=165)
    blood_type_var = StringVar(add_user_window)
    blood_type_var.set("O")  # Set default value
    blood_type_dropdown = OptionMenu(add_user_window, blood_type_var, "O", "A", "B", "AB")
    blood_type_dropdown.config(width=20, font=('Arial', 12))
    blood_type_dropdown.place(x=120, y=160)

    # Birthdate
    Label(add_user_window, text="Birthdate       :", font=('Helvetica', 12)).place(x=10, y=210)

    # Year Dropdown
    Label(add_user_window, text="Year :", font=('Helvetica', 12)).place(x=120, y=210)
    year_var = StringVar(add_user_window)
    years = [str(year) for year in range(1950, date.today().year + 1)]
    year_dropdown = Combobox(add_user_window, textvariable=year_var, values=years, state="readonly", width=5,
                             font='Arial 12')
    year_dropdown.place(x=170, y=210)

    # Month Dropdown
    Label(add_user_window, text="Month :", font=('Helvetica', 12)).place(x=250, y=210)
    month_var = StringVar(add_user_window)
    months = [str(month) for month in range(1, 13)]
    month_dropdown = Combobox(add_user_window, textvariable=month_var, values=months, state="readonly", width=3,
                              font='Arial 12')
    month_dropdown.place(x=310, y=210)

    # Day Dropdown
    Label(add_user_window, text="Day :", font=('Helvetica', 12)).place(x=370, y=210)
    day_var = StringVar(add_user_window)
    day_dropdown = Combobox(add_user_window, textvariable=day_var, state="readonly", width=3, font='Arial 12')
    day_dropdown.place(x=415, y=210)

    def update_day_dropdown(*args):
        selected_year = year_var.get()
        selected_month = month_var.get()
        if selected_year and selected_month:
            days_in_month = calendar.monthrange(int(selected_year), int(selected_month))[1]
            days = [str(day) for day in range(1, days_in_month + 1)]
            day_dropdown.config(values=days)
        else:
            day_dropdown.config(values=[])

    # Update day dropdown when year or month changes
    year_var.trace('w', update_day_dropdown)
    month_var.trace('w', update_day_dropdown)

    # Submit Button
    submit_button = Button(add_user_window, text="Submit", command=submit_user, height=1, width=10, font=('Arial', 12))
    submit_button.place(relx=0.5, rely=0.9, anchor=CENTER)

    add_user_window.mainloop()


def delete_user(user_id):
    # Function to delete a user from Firebase
    db.collection('user').document(user_id).delete()
    messagebox.showinfo("Success", "User deleted successfully")
    # Update user list display after deletion
    user_list()


def edit_user(uid):
    def submit_user_update():
        updated_user = {
            'name': name_entry.get(),
            'gender': gender_var.get(),
            'bloodType': blood_type_var.get(),
            # Add more fields as needed
        }

        db.collection('user').document(uid).update(updated_user)
        messagebox.showinfo("Success", "User updated successfully")
        # Clear form entries after submission
        name_entry.delete(0, END)
        # Update user list display
        user_list()
        edit_user_window.destroy()

    # Fetch current user details
    user_ref = db.collection('user').document(uid)
    user_data = user_ref.get().to_dict()

    # Create a Toplevel window for editing a user
    edit_user_window = Toplevel()
    edit_user_window.title("Edit User")
    edit_user_window.minsize(500, 300)
    edit_user_window.resizable(False, False)

    # Name
    Label(edit_user_window, text="Name         :", font=('Helvetica', 12)).place(x=50, y=50)
    name_entry = Entry(edit_user_window, width=25, font='Arial 15')
    name_entry.place(x=150, y=50)
    name_entry.insert(0, user_data['name'])

    # Gender
    Label(edit_user_window, text="Gender        :", font=('Helvetica', 12)).place(x=50, y=100)
    gender_var = StringVar(edit_user_window)
    gender_var.set(user_data['gender'])  # Set default value
    gender_dropdown = OptionMenu(edit_user_window, gender_var, "Male", "Female")
    gender_dropdown.config(width=20, font=('Arial', 12))
    gender_dropdown.place(x=150, y=100)

    # Blood Type
    Label(edit_user_window, text="Blood Type  :", font=('Helvetica', 12)).place(x=50, y=150)
    blood_type_var = StringVar(edit_user_window)
    blood_type_var.set(user_data['bloodType'])  # Set default value
    blood_type_dropdown = OptionMenu(edit_user_window, blood_type_var, "O", "A", "B", "AB")
    blood_type_dropdown.config(width=18, font=('Arial', 12))
    blood_type_dropdown.place(x=150, y=150)

    # Submit Button
    submit_button = Button(edit_user_window, text="Update", command=lambda: submit_user_update, height=1,
                           width=10,
                           font=('Arial', 12))
    submit_button.place(x=200, y=230)

    edit_user_window.mainloop()


nav_frame = Frame(admin_clinic, width=200, bg='#2a2a2a')
nav_frame.pack(fill='y', side='left')

content_area = Frame(admin_clinic, bg='white')
content_area.pack(fill='both', expand=True)

create_nav_button("Clinic List", clinic_list)
create_nav_button("Doctor List", doctor_list)
create_nav_button("User List", user_list)
create_nav_button("Log Out", log_out)

conn = initializeFirebase()
db = getClient()

admin_clinic.mainloop()
