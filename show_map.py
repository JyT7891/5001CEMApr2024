import tkinter as tk
from tkinter import messagebox
from geopy.geocoders import Nominatim
from tkintermapview import TkinterMapView
import sys
from run_script import run_script1
from fire_base import getClient, initializeFirebase

# Initialize the Firebase Admin SDK
conn = initializeFirebase()
db = getClient()


def getClinicName(clinic_id):
    """Fetch the clinic name from the database using the clinic ID."""
    try:
        clinic_doc = db.collection('clinic').document(clinic_id).get()
        if clinic_doc.exists:
            clinic_data = clinic_doc.to_dict()
            return clinic_data.get('name')
        else:
            return None
    except Exception as e:
        print(f"Error fetching clinic name: {str(e)}")
        return None


def show_location(clinic_id):
    """Show the location of the clinic on the map."""
    if not clinic_id:
        messagebox.showwarning("Input Error", "Please enter a clinic ID.")
        return

    clinic_name = getClinicName(clinic_id)
    if not clinic_name:
        messagebox.showerror("Clinic Not Found", "No clinic found with the specified ID.")
        return

    geolocator = Nominatim(user_agent="clinic_locator")
    location = geolocator.geocode(clinic_name)

    if location:
        map_widget.set_position(location.latitude, location.longitude)
        marker_text = f"{clinic_name}"  # Add additional information if available
        map_widget.set_marker(location.latitude, location.longitude, text=marker_text)
        map_widget.set_zoom(15)
    else:
        messagebox.showerror("Geocoding Error", "Could not find location for the clinic.")


def book_now_and_close(clinic_id, username):
    """Book the appointment and close the map window."""
    clinic_map.destroy()
    run_script1("user_appointment.py", clinic_id, username)


def cancel_book(username):
    """Cancel the booking and close the map window."""
    clinic_map.destroy()
    run_script1("user_home_page.py", username)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python show_map.py <clinic_id> <username>")
        sys.exit(1)

    clinic_id = sys.argv[1]
    username = sys.argv[2]

    # Create the main window
    clinic_map = tk.Tk()
    clinic_map.title("Clinic Locator")

    clinic_name = getClinicName(clinic_id)
    if clinic_name:
        tk.Label(clinic_map, text=f"Clinic ID : {clinic_name}", font=('Helvetica', 25, 'bold')).pack(pady=10)
    else:
        messagebox.showerror("Clinic Not Found", "No clinic found with the specified ID.")
        sys.exit(1)

    # Buttons for booking and canceling
    book_now = tk.Button(clinic_map, text="Book Now", font=('Helvetica', 10),
                         command=lambda: book_now_and_close(clinic_id, username))
    book_now.pack(pady=5)

    cancel = tk.Button(clinic_map, text="Cancel Book", font=('Helvetica', 10), command=lambda: cancel_book(username))
    cancel.pack(pady=5)

    # Map widget
    map_widget = TkinterMapView(clinic_map, width=600, height=400)
    map_widget.pack(pady=20)

    # Show the clinic location on the map
    show_location(clinic_id)
    clinic_map.mainloop()
