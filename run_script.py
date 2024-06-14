import argparse
import subprocess
import os
import sys


def run_script1(script_name, *args):
    # Path to the Python executable in your virtual environment
    python_executable = os.path.join(os.getcwd(), '.venv', 'Scripts', 'python.exe')

    # Ensure the script exists in the current directory
    script_path = os.path.join(os.getcwd(), script_name)

    # Check if the script file exists
    if not os.path.isfile(script_path):
        print(f"Error: Script '{script_path}' not found.")
        sys.exit(1)

    # Run the script using subprocess
    try:
        command = [python_executable, script_path] + list(args)
        result = subprocess.run(command, capture_output=True, text=True)
        result.check_returncode()  # This will raise an exception if the script returns a non-zero exit code
        print(f"Script output:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error running script '{script_name}': {e.stderr}")
    except FileNotFoundError:
        print(f"Error: Python executable '{python_executable}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Use argparse to handle command-line arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a Python script in a virtual environment.")
    parser.add_argument('script_name', type=str, help="The name of the script to run (e.g., 'sign_up.py').")
    parser.add_argument('script_args', nargs=argparse.REMAINDER, help="Additional arguments to pass to the script.")

    args = parser.parse_args()

    # Run the specified script with any additional arguments
    run_script1(args.script_name, *args.script_args)