import subprocess


class main():
    prompts = [
        "read the contents of main.py",
        "write 'hello' to main.txt",
        "run main.py",
        "list the contents of the pkg directory"
    ]

    for prompt in prompts:
        args = ["uv", "run", "main.py", prompt]
        op = subprocess.run(
            args,
            timeout=30,
            capture_output=True,
        )
        print(f"Prompt: {prompt}\nSTDOUT: {op.stdout}\n")


main()
