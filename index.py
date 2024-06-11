from tkinter import Tk, Frame
from side_bar import create_button
import home_page

# Initialize the main window
home_page = Tk()
home_page.minsize(1000, 790)
home_page.resizable(False, False)
home_page.title("Call A Doctor")

# Create a Frame for the sidebar
sidebar = Frame(home_page, width=200, bg="lavender")
sidebar.pack(fill='y', side='left')

# Load and display the logo
# logo_image = PhotoImage(file="cad1.png")
# logo_label = Label(sidebar, image=logo_image, bg="lavender")
# logo_label.pack(pady=10, padx=10)

# Main content area
content_area = Frame(home_page, bg="white", padx=20, pady=20)
content_area.pack(expand=True, fill="both")

# Create buttons for navigation
create_button(sidebar, "Home", lambda: home_page.open_home(content_area))
create_button(sidebar, "Search for Clinic", lambda: home_page.search_clinic(content_area))
# Add other buttons similarly

# Run the main event loop
home_page.mainloop()
