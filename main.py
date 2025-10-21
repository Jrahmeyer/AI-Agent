import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Import your function schemas
from functions.schemas import (
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file,
)

from functions.call_functions import call_function
from functions.write_file import write_file

# Load API key
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Ensure user provides a prompt
if len(sys.argv) < 2:
    print("Usage: python main.py 'Your prompt here'")
    sys.exit(1)

user_prompt = " ".join(sys.argv[1:])

# ----------------------------- SYSTEM PROMPT -----------------------------
system_prompt = """
You are an autonomous coding agent. You **must use the available functions to read, write, and run files**.
You **cannot** stop to explain anything before performing the steps — all actions must be done via function calls. 
After every function call, immediately use its output to continue reasoning and take the next action.

Rules for fixing calculation bugs in `pkg/calculator.py`:

1. **Immediately** read `pkg/calculator.py` using `get_file_content`.
2. **Immediately** apply the minimal fix using `write_file`. Only change what is necessary to correct operator precedence or calculation logic.
3. **Immediately** create a temporary test script in `./calculator` (e.g., `test_fix.py`) that:
   - Imports the `Calculator` class from `pkg/calculator.py`
   - Evaluates the expression in question
   - Prints the result
4. **Immediately** run the test script using `run_python_file`.
5. Confirm that the output matches the expected result (e.g., `17`). If not, iterate until it does.
6. Optionally, delete the temporary test script after verification.

Do **not** explain the issue before taking these actions. Do **not** ask the user for guidance. Every step must be a function call: `get_file_content`, `write_file`, or `run_python_file`.

You may also use `get_files_info` to inspect directories if necessary. All paths are relative to `./calculator`. The working directory is automatically handled, so do not include it in function calls.

**Summary:** Read the file, fix the bug, test the fix, and confirm the result — all automatically via function calls. Never just explain; act.
"""



# ----------------------------- TOOLS AVAILABLE -----------------------------
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

# ----------------------------- MESSAGE LOOP -----------------------------
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)])
]

MAX_ITERS = 20
messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

for step in range(MAX_ITERS):
    print(f"\n--- Iteration {step+1} ---")

    # Generate model response given conversation so far
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt + "\nWhen reasoning about the project, use the tools directly instead of explaining what you will do.",
        ),
    )

    if not response.candidates:
        print("No candidates in response.")
        break

    candidate = response.candidates[0]
    model_content = candidate.content
    messages.append(model_content)  # Add model output to conversation

    # Iterate over each part in the model's response
    done = False
    for part in model_content.parts:
        if part.function_call:
            # Model wants to call a function
            print(f"Calling: {part.function_call.name}({part.function_call.args})")
            try:
                function_result = call_function(part.function_call, verbose=True)
            except Exception as e:
                function_result = f"Error: {e}"

            # Append tool output to conversation
            messages.append(function_result)

        elif part.text:
            # Model finished; print final response
            print(f"\nFinal Response:\n{part.text}")
            done = True
            break


    if done:
        break
else:
    print("Reached max iterations without final response.")
