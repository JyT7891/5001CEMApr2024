import tkinter as tk
from tkinter import messagebox
from geopy.geocoders import Nominatim
from tkintermapview import TkinterMapView


# Function to get location and show on map
def show_location():
    clinic_name = entry.get()
    if not clinic_name:
        messagebox.showwarning("Input Error", "Please enter a clinic name.")
        return

    # Example: Fetching clinic details (replace with your actual data retrieval)
    # For demonstration, I'm using dummy data
    clinic_details = {
        'name': clinic_name,
        'phone': '123-456-7890',  # Replace with actual phone number retrieval
    }

    # Geocode the clinic name
    geolocator = Nominatim(user_agent="clinic_locator")
    location = geolocator.geocode(clinic_name)

    if location:
        # Set the map position to the clinic's location
        map_widget.set_position(location.latitude, location.longitude)

        # Add marker with clinic name and phone number
        marker_text = f"{clinic_details['name']}\nPhone: {clinic_details['phone']}"
        map_widget.set_marker(location.latitude, location.longitude, text=marker_text)

        # Adjust map zoom level (optional)
        map_widget.set_zoom(15)  # Adjust zoom level as needed
    else:
        messagebox.showerror("Geocoding Error", "Could not find location for the clinic.")


# Set up Tkinter GUI
root = tk.Tk()
root.title("Clinic Locator")

tk.Label(root, text="Enter Clinic Name:").pack(pady=10)
entry = tk.Entry(root, width=50)
entry.pack(pady=5)

tk.Button(root, text="Show Location", command=show_location).pack(pady=20)

# Create a map widget with smaller size
map_widget = TkinterMapView(root, width=600, height=400)
map_widget.pack(pady=20)

root.mainloop()
