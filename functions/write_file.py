import os

def write_file(working_directory, file_path, content):
    try:
        # Ensure working_directory itself exists
        os.makedirs(working_directory, exist_ok=True)

        # Get absolute paths
        working_directory = os.path.abspath(working_directory)

        # If the given file_path is relative, join it to working_directory
        if not os.path.isabs(file_path):
            abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        else:
            abs_file_path = os.path.abspath(file_path)

        # Ensure file_path is inside working_directory
        if not abs_file_path.startswith(working_directory + os.sep):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # Create parent directories of the target file if needed
        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)

        # Write content to the file (overwrite mode)
        with open(abs_file_path, "w", encoding="utf-8") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"
