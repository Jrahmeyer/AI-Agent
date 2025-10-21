import os

def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.join(working_directory, directory)

        abs_working_directory = os.path.abspath(working_directory)
        abs_target_directory = os.path.abspath(full_path)

        # Ensuring directory stays within working_directory
        if not abs_target_directory.startswith(abs_working_directory + os.sep) and abs_target_directory != abs_working_directory:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Ensuring its actually a directory
        if not os.path.isdir(abs_target_directory):
            return f'Error: "{directory}" is not a directory'
        
        # Build directory contents
        entries = []
        for entry in sorted(os.listdir(abs_target_directory)):
            entry_path = os.path.join(abs_target_directory, entry)
            try:
                size = os.path.getsize(entry_path)
                is_dir = os.path.isdir(entry_path)
                entries.append(f"- {entry}: file_size={size} bytes, is_dir={is_dir}")
            except Exception as e:
                entries.append(f"- {entry}: Error: {str(e)}")

        return "\n".join(entries)

    except Exception as e:
        return f"Error: {str(e)}"

    