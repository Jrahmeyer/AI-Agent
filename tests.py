from functions.write_file import write_file
from functions.run_python_file import run_python_file

def run_tests():
    # --- Existing write_file tests ---
    print('write_file("calculator", "lorem.txt", "wait, this isn\'t lorem ipsum"):')
    result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print(result)

    print('\nwrite_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"):')
    result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print(result)

    print('\nwrite_file("calculator", "/tmp/temp.txt", "this should not be allowed"):')
    result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print(result)

    # --- New run_python_file tests ---
    print('\nrun_python_file("calculator", "main.py"):')
    result = run_python_file("calculator", "main.py")
    print(result[:1000] + ("\n...[output truncated for display]" if len(result) > 1000 else ""))

    print('\nrun_python_file("calculator", "main.py", ["3 + 5"]):')
    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print(result[:1000] + ("\n...[output truncated for display]" if len(result) > 1000 else ""))

    print('\nrun_python_file("calculator", "tests.py"):')
    result = run_python_file("calculator", "tests.py")
    print(result[:1000] + ("\n...[output truncated for display]" if len(result) > 1000 else ""))

    print('\nrun_python_file("calculator", "../main.py"):')
    result = run_python_file("calculator", "../main.py")
    print(result)

    print('\nrun_python_file("calculator", "nonexistent.py"):')
    result = run_python_file("calculator", "nonexistent.py")
    print(result)

if __name__ == "__main__":
    run_tests()
