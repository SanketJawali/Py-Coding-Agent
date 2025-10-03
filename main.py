import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import get_files_info


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
    )

    print(response.text)

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


# Test code
# def temp():
#     print(get_files_info("calculator", "."))
#     print(get_files_info("calculator", "pkg"))


if __name__ == "__main__":
    main()
