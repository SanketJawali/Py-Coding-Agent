import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file


system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan.
You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory.
You do not need to specify the working directory in your function calls as
it is automatically injected for security reasons.
You must specify the directory you want to work in relative to the working directory.
If you want to work in the root of working directory then call functions with "." as
the directory you want to access.
Always specify file extensions as well whenever you want to work with files.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]
)


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"""
            Calling function: {function_call_part.name}({function_call_part.args})
        """)
    else:
        print(f" - Calling function: {function_call_part.name}")


def main():
    # Getting command line arguments
    args = sys.argv

    # Loading the env and gettig the variables
    load_dotenv()
    apiKey = os.environ.get("GEMINI_API_KEY")

    # Creating a client using api key
    client = genai.Client(api_key=apiKey)

    # Checking the prompt
    if not len(args) > 1:
        print("No prompt provided.")
        return

    prompt = args[1]

    # Verbose flag
    verboseFlag = False
    if len(args) == 3 and args[2] == "--verbose":
        verboseFlag = True

    # History
    messages = [
        types.Content(role="User", parts=[
            types.Part(text=prompt)
        ]),
    ]

    # Calling api and printing response
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        )
    )

    print("LLM Text Response: ", response.text)
    function_call_part = response.function_calls[0]
    print(f"Calling function: {
          function_call_part.name}({function_call_part.args})")

    # Handle bad response
    if response is None or response.usage_metadata is None:
        print("Bad Response. Missing response or missing metadata.")
        return

    # printing prompt token cost
    if verboseFlag:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {
              response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
