import subprocess
import os
import sys


def run_script1(script_name, *args):
    python_executable = os.path.join(os.getcwd(), '.venv', 'Scripts', 'python.exe')
    script_path = os.path.join(os.getcwd(), script_name)

    if not os.path.isfile(script_path):
        print(f"Error: Script '{script_path}' not found.")
        sys.exit(1)

    try:
        command = [python_executable, script_path] + list(args)
        print(f"Running command: {command}")
        result = subprocess.run(command, capture_output=True, text=True)
        result.check_returncode()
        print(f"Script output:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error running script '{script_name}': {e.stderr}")
    except FileNotFoundError:
        print(f"Error: Python executable '{python_executable}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_script.py <script_name> [<script_args>...]")
        sys.exit(1)

    script_name = sys.argv[1]
    script_args = sys.argv[2:]

    run_script1(script_name, *script_args)
