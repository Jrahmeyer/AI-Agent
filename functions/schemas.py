from google.genai import types

# Get files info
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

# Read file contents
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the contents of a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)

# Run a Python file
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file with optional arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the Python file to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of arguments to pass to the Python file.",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
        required=["file_path"],
    ),
)

# Write or overwrite file
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=(
        "Writes or overwrites a file in the calculator project with the provided content. "
        "Use this to apply bug fixes, modify existing source code, or create new files. "
        "Always provide the complete updated content for the file, not just a diff. "
        "All paths must be relative to the ./calculator working directory."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=(
                    "Relative path to the file to write inside the ./calculator directory, "
                    "for example 'pkg/calculator.py'."
                ),
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description=(
                    "The full new content of the file (complete replacement). "
                    "Include any code edits necessary to implement a fix or feature."
                ),
            ),
        },
        required=["file_path", "content"],
    ),
)
