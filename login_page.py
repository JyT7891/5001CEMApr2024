import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from fire_base import getClient, initializeFirebase
from run_script import run_script1

# Initialize the Firebase Admin SDK
conn = initializeFirebase()
db = getClient()

# Create the main Tkinter window
patient_login = tk.Tk()
patient_login.minsize(1000, 790)
patient_login.resizable(False, False)
patient_login.title("Login")

# Load and display an image
image = Image.open('CAD.png')
image = ImageTk.PhotoImage(image)

image_label = tk.Label(patient_login, image=image)
image_label.place(x=220, y=-180)


# Function to check if an email exists in Firestore
def email_exists_in_firestore(username1):
    try:
        doc_ref = db.collection('user').document(username1)  # Adjust the path as per your Firestore structure
        doc = doc_ref.get()
        return doc.exists
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def password_matches(username1, password):
    try:
        doc_ref = db.collection('user').document(username1)  # Adjust the path as per your Firestore structure
        doc = doc_ref.get()
        if doc.exists:
            user_data = doc.to_dict()
            # Close the current Tkinter window
            patient_login.destroy()
            messagebox.showinfo("Login Successful", "Login successful!")
            return user_data.get('password') == password
        else:
            doc_ref = db.collection('doctor').document(username1)  # Adjust the path as per your Firestore structure
            doc = doc_ref.get()
            if doc.exists:
                user_data = doc.to_dict()
                # Close the current Tkinter window
                patient_login.destroy()
                run_script1('doctor_web.py')
                messagebox.showinfo("Login Successful", "Login successful!")
                return user_data.get('password') == password
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


# Function to handle login process
def check_login(event=None):
    username1 = insert_username.get()
    password = insert_password.get()

    if email_exists_in_firestore(username1):
        if password_matches(username1, password):
            run_script1('user_home_page.py', username1)
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")
    else:
        messagebox.showerror("Login Failed", "Email does not exist. Please sign up.")


# Function to handle sign-up process
def check_sign_up():
    # Close the current Tkinter window
    patient_login.destroy()
    # Call the function to run the script
    run_script1('sign_up.py')


# Function to create a rounded rectangle on a canvas
def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    points = [
        x1 + radius, y1,
        x1 + radius, y1,
        x2 - radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1 + radius,
        x1, y1,
    ]
    return canvas.create_polygon(points, **kwargs, smooth=True)


# Function to set up the login page
def login_page():
    global insert_username, insert_password

    # Styling inspired by UHS Inc.
    patient_login.configure(bg='#f2f2f2')  # Light grey background

    # Create a canvas for the rounded rectangle
    canvas = tk.Canvas(patient_login, bg='#f2f2f2', highlightthickness=0)
    canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=500, height=400)

    # Create the rounded rectangle
    create_rounded_rectangle(canvas, 0, 0, 500, 400, radius=25, fill='#ffffff', outline='')

    # Frame for the login form
    login_frame = tk.Frame(canvas, bg='#ffffff')
    login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=480, height=380)

    # Title label
    title_label = tk.Label(login_frame, text="User Login", font=('Helvetica', 26, 'bold'), bg='#ffffff', fg='#333333')
    title_label.pack(pady=20)

    # Username label and entry
    username_label = tk.Label(login_frame, text="Username", font=('Helvetica', 14), bg='#ffffff', fg='#333333')
    username_label.pack(pady=10)
    insert_username = ttk.Entry(login_frame, font=('Helvetica', 14))
    insert_username.pack(pady=10)

    # Password label and entry
    password_label = tk.Label(login_frame, text="Password", font=('Helvetica', 14), bg='#ffffff', fg='#333333')
    password_label.pack(pady=10)
    insert_password = ttk.Entry(login_frame, font=('Helvetica', 14), show="*")
    insert_password.pack(pady=10)

    # Sign Up button
    sign_up_button = ttk.Button(login_frame, text="Sign Up", command=check_sign_up)
    sign_up_button.pack(side=tk.LEFT, padx=20, pady=20)

    # Login button
    login_button = ttk.Button(login_frame, text="Login", command=check_login)
    login_button.pack(side=tk.RIGHT, padx=20, pady=20)

    # Bind the Return key to the login function
    patient_login.bind("<Return>", check_login)


def main():
    # Set up the login page
    login_page()

    # Run the Tkinter main loop
    patient_login.mainloop()


if __name__ == '__main__':
    main()
