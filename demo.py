import tkinter as tk
from tkinter import messagebox
import subprocess

def show_clinic_patient(script_name, clinic_id, patient_name):
    try:
        command = ['python', script_name, clinic_id, patient_name]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            messagebox.showerror("Error", f"Failed to run {script_name}:\n{result.stderr}")
        else:
            print(f"Output:\n{result.stdout}")  # Adjust this based on your application's needs
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Example usage within a Tkinter application
if __name__ == "__main__":
    script_name = "user_appointment.py"  # Replace with your actual script name
    clinic_id = "12345"  # Replace with actual clinic ID
    patient_name = "John Doe"  # Replace with actual patient name

    # Example call
    show_clinic_patient(script_name, clinic_id, patient_name)
