import os
from functions.config import MAX_FILE_CHARS

def get_file_content(working_directory, file_path):
    try:
        # Build the full path
        full_path = os.path.join(working_directory, file_path)

        # Normalize paths
        abs_working_dir = os.path.abspath(working_directory)
        abs_target_file = os.path.abspath(full_path)

        # Guardrail: ensure file is inside working_directory
        if not abs_target_file.startswith(abs_working_dir + os.sep) and abs_target_file != abs_working_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Ensure it’s a regular file
        if not os.path.isfile(abs_target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Read the file
        with open(abs_target_file, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        # Truncate if needed
        if len(content) > MAX_FILE_CHARS:
            truncated = content[:MAX_FILE_CHARS]
            truncated += f'\n[...File "{file_path}" truncated at {MAX_FILE_CHARS} characters]'
            return truncated

        return content

    except Exception as e:
        return f"Error: {str(e)}"
