import os
import sys
from dotenv import load_dotenv
from google import genai


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

    # Calling api and printing response
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", contents=prompt
    )

    print(response.text)

    # Handle bad response
    if (response == None) or (response.usage_metadata == None):
        print("Bad Response. Missing response or missing metadata.")
        return

    # printing prompt token cost
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
