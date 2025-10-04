import os
from google.genai import types


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="""This function is used to write content to a file, may it be a python file or any text file.
        This function can also create files if they didn't exist previously, along with the directories as well.
        The provided content will over-write the any previous contents of the spedified file.
    """,
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path is the path to any type of file relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="""Content or code to be writted within the specified file.
                    This content will over-write the previous contents of the file.
                    This function will also create the file if the file doesn't exist.
                """,
            ),
        },
    ),
)


def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # check if directory out of working directory
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    # if file doesn't exist, create it; else write content
    if not os.path.exists(abs_file_path):
        try:
            # crating the directory
            os.makedirs(os.path.dirname(abs_file_path))

            with open(abs_file_path, "x") as file:
                file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        except FileExistsError:
            return "Error: File creation failed as the file already exists."
        except Exception as err:
            return f"Error: Unexpected error occured while crating new file. {err}"
    else:
        try:
            with open(abs_file_path, "w") as file:
                file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        except Exception as err:
            return f"Error: Unexpected error occured while writing to file. {err}"
