import os
from google.genai import types

# Import your four function implementations
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

def call_function(function_call_part, verbose=False):
    """Handles execution of LLM-chosen functions safely."""

    function_name = function_call_part.name
    args = dict(function_call_part.args or {})

    # Add our enforced working directory
    args["working_directory"] = "./calculator"

    # Map names to actual callable functions
    functions = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }

    if verbose:
        print(f"Calling function: {function_name}({args})")
    else:
        print(f" - Calling function: {function_name}")

    # Check for invalid function names
    if function_name not in functions:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    # Attempt to execute the function
    try:
        func = functions[function_name]
        result = func(**args)
    except Exception as e:
        result = f"Error while executing {function_name}: {e}"

    # Return a proper tool response
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result},
            )
        ],
    )
