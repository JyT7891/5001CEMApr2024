import argparse
import subprocess
import os
import sys


def run_script1(script_name):
    # Path to the Python executable in your virtual environment
    python_executable = os.path.join(os.getcwd(), '.venv', 'Scripts', 'python.exe')

    # Ensure the script exists in the current directory
    script_path = os.path.join(os.getcwd(), script_name)
    # Run the script using subprocess
    result = subprocess.run([python_executable, script_path], capture_output=True, text=True)


# Use argparse to handle command-line arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a Python script in a virtual environment.")
    parser.add_argument('script_name', type=str, help="The name of the script to run (e.g., 'sign_up.py').")

    args = parser.parse_args()

    # Run the specified script
    run_script1(args.script_name)
