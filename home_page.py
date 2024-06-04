from tkinter import *

home_page = Tk()
home_page.minsize(1000, 790)
home_page.resizable(False, False)
home_page.title("Call A Doctor")


def on_enter(event):
    event.widget.config(width=15, height=2, font=('Helvetica', 12, 'bold'))


def on_leave(event):
    event.widget.config(width=20, height=1, font=('Helvetica', 12))


def on_click(event):
    event.widget.config(bg="blue")


def on_release(event):
    event.widget.config(bg="SystemButtonFace")


def open_home():
    # Function to open the home page
    print("Opening Home Page")


def open_settings():
    # Function to open the settings page
    print("Opening Settings Page")


def open_about():
    # Function to open the about page
    print("Opening About Page")


# Create a Frame for the sidebar
sidebar = Frame(home_page, width=200, bg="lavender")
sidebar.pack(fill=Y, side=LEFT)

# Create buttons for navigation
logo_image = PhotoImage(file="cad1.png")
logo_label = Label(sidebar, image=logo_image, bg="lavender")
logo_label.pack(pady=10, padx=10)


def button():
    home = Button(sidebar, text="Home", command=open_home)
    home.pack(pady=20)
    home.bind("<Enter>", on_enter)
    home.bind("<Leave>", on_leave)
    home.bind("<ButtonPress-1>", on_click)
    home.bind("<ButtonRelease-1>", on_release)

    search = Button(sidebar, text="Search for clinic", command=open_settings)
    search.pack(pady=20)
    search.bind("<Enter>", on_enter)
    search.bind("<Leave>", on_leave)
    search.bind("<ButtonPress-1>", on_click)
    search.bind("<ButtonRelease-1>", on_release)

    book_appointment = Button(sidebar, text="Book Appointment", command=open_about)
    book_appointment.pack(pady=20)
    book_appointment.bind("<Enter>", on_enter)
    book_appointment.bind("<Leave>", on_leave)
    book_appointment.bind("<ButtonPress-1>", on_click)
    book_appointment.bind("<ButtonRelease-1>", on_release)

    manage_appointment = Button(sidebar, text="Manage Appointment", command=open_about)
    manage_appointment.pack(pady=20)
    manage_appointment.bind("<Enter>", on_enter)
    manage_appointment.bind("<Leave>", on_leave)
    manage_appointment.bind("<ButtonPress-1>", on_click)
    manage_appointment.bind("<ButtonRelease-1>", on_release)

    profile = Button(sidebar, text="Profile", command=open_about)
    profile.pack(pady=20)
    profile.bind("<Enter>", on_enter)
    profile.bind("<Leave>", on_leave)
    profile.bind("<ButtonPress-1>", on_click)
    profile.bind("<ButtonRelease-1>", on_release)


# Main content area
button()
content_area = Frame(home_page, bg="white", padx=20, pady=20)
content_area.pack(expand=True, fill="both")

# Add widgets to the content area (your main application content)

home_page.mainloop()
