import os


def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # check if directory out of working directory
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    # if file doesn't exist, create it; else write content
    if not os.path.exists(abs_file_path):
        try:
            with open(abs_file_path, "x") as file:
                file.write(content)
            print(f'File "{file_path}" created successfully')
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
