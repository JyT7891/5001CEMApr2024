import sys
import os
from tkinter import *
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
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
    clear_content()

    # Header Frame
    header_frame = Frame(parent)
    header_frame.pack(fill='x', padx=20, pady=10)

    # Add Clinic Button in the Header Frame
    if item_type == 'clinic':
        add_clinic_button = Button(header_frame, text="Add Clinic", font=('Helvetica', 15), fg='white', bg='#07497d',
                                   command=add_clinic)
        add_clinic_button.pack(side="top", padx=10, pady=5)

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

    frame_width = 300
    frame_height = 200
    num_columns = 3

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

            # Delete button for clinics
            delete_button = Button(item_frame, text="Delete", bg="red", fg="white", width=10, height=5,
                                   font=('Helvetica', 15), command=lambda cid=item['clinic_id']: delete_clinic(cid))
            delete_button.pack(side="bottom", padx=5, pady=5)

        elif item_type == 'doctor':
            item_label = Label(item_frame, text=item['doc_name'], font=('Helvetica', 15, 'bold'), bg="#f0f0f0",
                               fg='#07497d')
            item_label.pack(anchor="w")
            item_detail_label = Label(item_frame, text=item['service'], font=('Helvetica', 12), bg="#f0f0f0",
                                      fg='#07497d')
            item_detail_label.pack(anchor="w")
            clinic_label = Label(item_frame, text=f"Clinic: {item['clinic_id']}", font=('Helvetica', 12), bg="#f0f0f0",
                                 fg='#07497d')
            clinic_label.pack(anchor="w", pady=2)
            availability_label = Label(item_frame, text=f"Available: {item['is_Available']}", font=('Helvetica', 12),
                                       bg="#f0f0f0", fg='#07497d')
            availability_label.pack(anchor="w", pady=2)

            # Delete button for doctors
            delete_button = Button(item_frame, text="Delete", bg="red", fg="white", command=lambda did=item['doc_name']: delete_doctor(did))
            delete_button.pack(side="bottom", pady=5)

        elif item_type == 'user':
            item_label = Label(item_frame, text=item['name'], font=('Helvetica', 15, 'bold'), bg="#f0f0f0",
                               fg='#07497d')
            item_label.pack(anchor="w")
            item_detail_label = Label(item_frame, text=f"Gender        : {item['gender']}", font=('Helvetica', 12),
                                      bg="#f0f0f0", fg='#07497d')
            item_detail_label.pack(anchor="w")
            blood_type_label = Label(item_frame, text=f"Blood Type : {item['bloodType']}", font=('Helvetica', 12),
                                     bg="#f0f0f0", fg='#07497d')
            blood_type_label.pack(anchor="w", pady=2)
            age_label = Label(item_frame, text=f"Age              : {item['age']}", font=('Helvetica', 12), bg="#f0f0f0",
                              fg='#07497d')
            age_label.pack(anchor="w", pady=2)

            # Delete button for users
            delete_button = Button(item_frame, text="Delete", bg="red", fg="white", command=lambda uid=item['username']: delete_user(uid))
            delete_button.pack(side="bottom", pady=5)

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


def add_clinic():

    # Function to add a new clinic to Firebase
    def submit_clinic():
        new_clinic = {
            'name': name_entry.get(),
            'phone_num': phone_entry.get(),
            'open_time': open_time_entry.get(),
            'close_time': close_time_entry.get()
            # Add more fields as needed
        }
        # Add new clinic to Firebase collection
        db.collection('clinic').add(new_clinic)
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
    Label(add_clinic_window, text="Clinic Name    : ", font=('Helvetica', 12)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
    name_entry = Entry(add_clinic_window, width=25, font='Arial 19')
    name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    # Phone Number
    Label(add_clinic_window, text="Phone Number    : ", font=('Helvetica', 12)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
    phone_entry = Entry(add_clinic_window, width=25, font='Arial 19')
    phone_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    # Open Time
    Label(add_clinic_window, text="Open Time      : ", font=('Helvetica', 12)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
    open_time_entry = Entry(add_clinic_window, width=25, font='Arial 19')
    open_time_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    # Close Time
    Label(add_clinic_window, text="Close Time      : ", font=('Helvetica', 12)).grid(row=3, column=0, padx=10, pady=5, sticky="e")
    close_time_entry = Entry(add_clinic_window, width=25, font='Arial 19')
    close_time_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    # Submit Button
    submit_button = Button(add_clinic_window, text="Submit", command=submit_clinic, height=1, width=10,
                           font=('Arial', 20))
    submit_button.grid(row=4, columnspan=2, padx=10, pady=10, ipadx=50)

    add_clinic_window.mainloop()


def delete_clinic(clinic_id):
    # Function to delete a clinic from Firebase
    db.collection('clinic').document(clinic_id).delete()
    messagebox.showinfo("Success", "Clinic deleted successfully")
    # Update clinic list display after deletion
    clinic_list()


def delete_doctor(doctor_id):
    # Function to delete a doctor from Firebase
    db.collection('doctor').document(doctor_id).delete()
    messagebox.showinfo("Success", "Doctor deleted successfully")
    # Update doctor list display after deletion
    doctor_list()


def delete_user(user_id):
    # Function to delete a user from Firebase
    db.collection('user').document(user_id).delete()
    messagebox.showinfo("Success", "User deleted successfully")
    # Update user list display after deletion
    user_list()


nav_frame = Frame(admin_clinic, width=200, bg='#2a2a2a')
nav_frame.pack(fill='y', side='left')

content_area = Frame(admin_clinic, bg='white')
content_area.pack(fill='both', expand=True)

create_nav_button("Clinic List", clinic_list)
create_nav_button("Doctor List", doctor_list)
create_nav_button("User List", user_list)
create_nav_button("Log Out", log_out)

add_clinic_button = Button(nav_frame, text="Add Clinic", font=('Helvetica', 20), fg='white', bg='#2a2a2a', command=add_clinic, relief='flat')
add_clinic_button.pack(fill='x', padx=20, pady=10)
add_clinic_button.bind("<Enter>", on_enter)
add_clinic_button.bind("<Leave>", on_leave)

conn = initializeFirebase()
db = getClient()

admin_clinic.mainloop()
