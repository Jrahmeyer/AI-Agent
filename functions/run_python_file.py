import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    try:
        # Resolve absolute paths
        working_directory = os.path.abspath(working_directory)

        if not os.path.isabs(file_path):
            abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        else:
            abs_file_path = os.path.abspath(file_path)

        # Ensure file_path is inside working_directory
        if not abs_file_path.startswith(working_directory + os.sep):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Check if file exists
        if not os.path.exists(abs_file_path):
            return f'Error: File "{file_path}" not found.'

        # Ensure file ends with .py
        if not abs_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        # Run the Python file
        completed_process = subprocess.run(
            ["python3", abs_file_path] + args,
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=30
        )

        # Format output
        stdout = completed_process.stdout.strip()
        stderr = completed_process.stderr.strip()

        output_parts = []
        if stdout:
            output_parts.append(f"STDOUT:\n{stdout}")
        if stderr:
            output_parts.append(f"STDERR:\n{stderr}")
        if completed_process.returncode != 0:
            output_parts.append(f"Process exited with code {completed_process.returncode}")

        if not output_parts:
            return "No output produced."

        return "\n".join(output_parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"
