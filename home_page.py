from tkinter import *

# Initialize the main window
home_page = Tk()
home_page.minsize(1000, 790)
home_page.resizable(False, False)
home_page.title("Call A Doctor")

# Define button events
def on_enter(event):
    event.widget.config(width=20, height=2, font=('Helvetica', 12, 'bold'))

def on_leave(event):
    event.widget.config(width=15, height=2, font=('Helvetica', 10))

def on_click(event):
    event.widget.config(bg="blue")

def on_release(event):
    event.widget.config(bg="SystemButtonFace")

# Define button command functions
def open_home():
    print("Opening Home Page")

def search_clinic():
    print("Searching for Clinic")

def book_appointment():
    print("Booking Appointment")

def manage_appointment():
    print("Managing Appointment")

def open_profile():
    print("Opening Profile")

# Create a Frame for the sidebar
sidebar = Frame(home_page, width=200, bg="lavender")
sidebar.pack(fill=Y, side=LEFT)

# Load and display the logo
logo_image = PhotoImage(file="cad1.png")
logo_label = Label(sidebar, image=logo_image, bg="lavender")
logo_label.pack(pady=10, padx=10)

# Function to create and pack buttons with events
def create_button(text, command):
    button = Button(sidebar, text=text, command=command, width=20, height=2, font=('Helvetica', 10))
    button.pack(pady=20)
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)
    button.bind("<ButtonPress-1>", on_click)
    button.bind("<ButtonRelease-1>", on_release)
    return button

# Create buttons for navigation
create_button("Home", open_home)
create_button("Search for Clinic", search_clinic)
create_button("Book Appointment", book_appointment)
create_button("Manage Appointment", manage_appointment)
create_button("Profile", open_profile)

# Main content area
content_area = Frame(home_page, bg="white", padx=20, pady=20)
content_area.pack(expand=True, fill="both")

# Add widgets to the content area (your main application content)

# Run the main event loop
home_page.mainloop()
