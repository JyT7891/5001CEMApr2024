import tkinter as tk
from tkinter import messagebox
from geopy.geocoders import Nominatim
from tkintermapview import TkinterMapView
import sys
from run_script import run_script1

def show_location(clinic_name):
    if not clinic_name:
        messagebox.showwarning("Input Error", "Please enter a clinic name.")
        return

    geolocator = Nominatim(user_agent="clinic_locator")
    location = geolocator.geocode(clinic_name)

    if location:
        map_widget.set_position(location.latitude, location.longitude)
        marker_text = f"{clinic_name}\nPhone: 123-456-7890"
        map_widget.set_marker(location.latitude, location.longitude, text=marker_text)
        map_widget.set_zoom(15)
    else:
        messagebox.showerror("Geocoding Error", "Could not find location for the clinic.")

def book_now_and_close():
    clinic_map.destroy()
    run_script1("user_appointment.py", clinic_name)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python show_map.py <clinic_name>")
        sys.exit(1)
    clinic_name = sys.argv[1]

    clinic_map = tk.Tk()
    clinic_map.title(clinic_name)

    tk.Label(clinic_map, text=f"Clinic Name : {clinic_name}", font=('Helvetica', 25, 'bold')).pack(pady=10)
    book_now = tk.Button(clinic_map, text="Book Now", font=('Helvetica', 10), command=book_now_and_close)
    book_now.pack(pady=5)

    map_widget = TkinterMapView(clinic_map, width=600, height=400)
    map_widget.pack(pady=20)

    show_location(clinic_name)
    clinic_map.mainloop()
