import os
import subprocess
from google.genai import types


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a python file with it's file path, constrained to the working directory. Pass in optional arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path is the path to a python file relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="Optional arguments passed to the python file while execution as command line arguments",
            ),
        },
    ),
)


def run_python_file(working_directory: str, file_path: str, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'

    if not abs_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    # running the python file
    try:
        arg = ["python3", abs_file_path],
        arg += args

        op = subprocess.run(
            arg,
            timeout=30,
            capture_output=True,
            cwd=abs_working_dir
        )

        if len(op.stdout) == 0:
            result = "No output produced."
        else:
            result = f"""STDOUT: {op.stdout}\nSTDERR: {op.stderr}"""

        if not op.returncode == 0:
            result += f"Process exited with code {op.returncode}"

        return result

    except Exception as err:
        return f"Error: executing Python file: {err}"
