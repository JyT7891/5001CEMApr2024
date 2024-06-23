import sys
from tkinter import *
from tkinter import messagebox
from datetime import datetime
from fire_base import getClient, initializeFirebase

# Initialize the Firebase Admin SDK
conn = initializeFirebase()
db = getClient()


def generate_report(username, patient_name, doc_id):
    report_text = report_textbox.get("1.0", "end-1c")

    if report_text:
        try:
            # Prepare report data
            report_data = {
                'patient_name': patient_name,
                'report_text': report_text,
                'report_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            # Retrieve doctor document reference
            doctor_doc_ref = db.collection('doctor').document(username)

            # Retrieve the doctor's current appointments
            doctor_doc = doctor_doc_ref.get()
            if doctor_doc.exists:
                doctor_data = doctor_doc.to_dict()
                appointments = doctor_data.get('appointments', [])

                # Update the specific appointment with the new report
                for appointment in appointments:
                    if appointment['doc_id'] == doc_id and appointment['patient_name'] == patient_name:
                        if 'reports' not in appointment:
                            appointment['reports'] = []
                        appointment['reports'].append(report_data)
                        break

                # Update the appointments in Firestore
                doctor_doc_ref.update({'appointments': appointments})

                messagebox.showinfo("Success", "Report generated and appointment updated successfully.")

                # Clear fields after submission
                report_textbox.delete("1.0", "end")

            else:
                messagebox.showerror("Error", "Doctor profile not found.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save report: {str(e)}")
    else:
        messagebox.showwarning("Warning", "Report text cannot be empty.")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python patient_report.py <username> <appointment_index>")
        sys.exit(1)

    username = sys.argv[1]
    index = int(sys.argv[2])

    # Retrieve the doctor's current appointments
    doctor_doc_ref = db.collection('doctor').document(username)
    doctor_doc = doctor_doc_ref.get()
    if doctor_doc.exists:
        doctor_data = doctor_doc.to_dict()
        appointments = doctor_data.get('appointments', [])

        if 0 <= index < len(appointments):
            appointment = appointments[index]
            patient_name = appointment['patient_name']
            doc_id = appointment['doc_id']
        else:
            print("Invalid appointment index.")
            sys.exit(1)
    else:
        print("Doctor profile not found.")
        sys.exit(1)

    # Initialize Tkinter
    doc_report = Tk()
    doc_report.title(f"Doctor's Report - {username}")
    doc_report.minsize(800, 600)
    doc_report.resizable(False, False)

    # Patient Name
    Label(doc_report, text=f"Patient Name: {patient_name}", font=('Helvetica', 12)).pack(anchor='w', padx=10, pady=10)

    # Report Text
    Label(doc_report, text="Report:", font=('Helvetica', 12)).pack(anchor='w', padx=10, pady=10)
    report_textbox = Text(doc_report, width=60, height=10, font='Arial 12')
    report_textbox.pack(anchor='w', padx=10, pady=10)

    # Generate Report Button
    generate_button = Button(doc_report, text="Generate Report",
                             command=lambda: generate_report(username, patient_name, doc_id), font=('Arial', 12))
    generate_button.pack(pady=20)

    doc_report.mainloop()
