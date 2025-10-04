import os
from google.genai import types


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


def get_files_info(working_directory, directory="."):
    abs_working_dir = os.path.abspath(working_directory)

    if directory is None:
        directory = "."

    # Joining working dir and dir to ensure dir is within working_directory
    abs_dir = os.path.abspath(os.path.join(working_directory, directory))
    # print(f"dir: {abs_dir}, wdir: {abs_working_dir}")

    # check if directory is valid
    if not os.path.isdir(abs_dir):
        return f'Error: "{directory}" is not a directory'

    if not abs_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    # list directory content
    ls = os.listdir(abs_dir)
    if len(ls) < 1:
        return "The directory is empty"

    # print the content of the directory with more info
    response = ""

    if directory == ".":
        print("Results for current directory:")
    else:
        print(f"Results for {directory} directory:")

    for item in ls:
        itemPath = os.path.join(abs_dir, item)
        size = os.path.getsize(itemPath)
        isDir = os.path.isdir(itemPath)

        response += f"- {item}: file_size={size} bytes, is_dir={isDir}\n"

    return response
