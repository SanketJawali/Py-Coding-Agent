import os
from functions.config import MAX_FILE_CHARS
from google.genai import types


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="""Get the contents of any type of file.
        Files only within the working directory are accessible, with only first 10,000 characters can be output.
    """,
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path is the path to a python file relative to the working directory.",
            ),
        },
    ),
)


def get_file_content(working_directory, file_path):
    if not working_directory or not file_path:
        return "Error: Working directory or file path not provided"

    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    # Reading file
    try:
        with open(abs_file_path, "r") as f:
            file_content_string = f.read(MAX_FILE_CHARS)

            # if file > 10k char; return first 10k char
            if len(file_content_string) >= MAX_FILE_CHARS:
                content = file_content_string[:MAX_FILE_CHARS] + \
                    f'[...File "{file_path}" truncated at 10000 characters]'
                return content

            return file_content_string
    except Exception as err:
        return f"Error: Unexpected error occured, {err}"
