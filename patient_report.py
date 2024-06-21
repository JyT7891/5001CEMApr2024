import sys
from tkinter import *
from tkinter import messagebox
from datetime import datetime
from run_script import run_script1
from fire_base import getClient, initializeFirebase

# Initialize the Firebase Admin SDK
conn = initializeFirebase()
db = getClient()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python doctor_web.py <username>")

    username = sys.argv[1]

    # Initialize Tkinter
    doc_report = Tk()
    doc_report.title(f"Report")
    doc_report.minsize(1250, 790)
    doc_report.resizable(False, False)
