from tkinter import *
from tkinter import messagebox
from datetime import datetime
from run_script import run_script1

# Global list to store appointments
appointments = []

# Initialize Tkinter
doctor = Tk()
doctor.title("Doctor Appointment System")
doctor.minsize(1250, 790)
doctor.resizable(False, False)


# Function to view all appointments
def view_appointments():
    if not appointments:
        messagebox.showinfo("Appointments", "No appointments found")
        return

    appointments_str = "\n".join([
        f"{a['name']}: {a['status']} - Check-in: {a.get('check_in_time', 'N/A')} - Check-out: {a.get('check_out_time', 'N/A')}"
        for a in appointments])
    messagebox.showinfo("Appointments", appointments_str)


# Variable to track doctor's availability
doctor_available = True

# Global variable for availability label
availability_label = None


# Function to toggle doctor's availability
def toggle_availability():
    global doctor_available
    doctor_available = not doctor_available
    availability_label.config(text=f"Doctor is {'Available' if doctor_available else 'Not Available'}")


# Function to handle check-in process
def check_in():
    if not doctor_available:
        messagebox.showerror("Error", "Doctor is not available.")
        return

    name = name_entry.get()
    if name:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        appointments.append({'name': name, 'status': 'Checked In', 'check_in_time': current_time})
        messagebox.showinfo("Success", f"Checked in {name} at {current_time}")
    else:
        messagebox.showerror("Error", "Please enter a name")


# Function to handle check-out process
def check_out():
    if not doctor_available:
        messagebox.showerror("Error", "Doctor is not available.")
        return

    name = name_entry.get()
    for appointment in appointments:
        if appointment['name'] == name and appointment['status'] == 'Checked In':
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            appointment['status'] = 'Checked Out'
            appointment['check_out_time'] = current_time
            messagebox.showinfo("Success", f"Checked out {name} at {current_time}")
            return
    messagebox.showerror("Error", "No checked-in appointment found for this name")


# Function to handle clock in/out operations
def clock_in_out():
    global name_entry
    clear_content()

    # Doctor availability toggle button
    availability_button = Button(content_area, text="Toggle Availability", command=toggle_availability)
    availability_button.pack(pady=5)

    # Label to display doctor's availability status
    availability_label = Label(content_area, text="Doctor is Available", fg="green" if doctor_available else "red")
    availability_label.pack(pady=5)

    # Patient Name Entry
    name_label = Label(content_area, text="Doctor Name:")
    name_label.pack()
    name_entry = Entry(content_area)
    name_entry.pack()

    # Check-in Button
    check_in_button = Button(content_area, text="Check In", command=check_in)
    check_in_button.pack(pady=5)

    # Check-out Button
    check_out_button = Button(content_area, text="Check Out", command=check_out)
    check_out_button.pack(pady=5)


def check_appointment():
    pass


def open_profile():
    pass


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
create_button("Profile", open_profile)
create_button("Log Out", log_out)

# Start the main loop
doctor.mainloop()
