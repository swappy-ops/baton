import ollama
import subprocess

client = ollama.Client(
    host='http://192.168.1.19:11434'
)

TOOLS = {
    "list_files":"ls",
    "current_directory":"pwd"
}

while True:

    task=input("\nTask: ")

    if task=="exit":
        break

    planner=client.chat(
        model='qwen2.5-coder:7b',
        messages=[
            {
                "role":"system",
                "content":f"""
You are an agent.

Available tools:
{TOOLS}

Reply ONLY with:
- tool:list_files
OR
- tool:current_directory
OR
- no_tool
"""
            },
            {
                "role":"user",
                "content":task
            }
        ]
    )

    decision=planner[
        "message"
    ]["content"].strip()

    print("\nDecision:",decision)

    if "tool:list_files" in decision:

        result=subprocess.check_output(
            "ls",
            shell=True
        ).decode()

        print("\nTOOL OUTPUT:\n")
        print(result)

    elif "tool:current_directory" in decision:

        result=subprocess.check_output(
            "pwd",
            shell=True
        ).decode()

        print("\nTOOL OUTPUT:\n")
        print(result)

    else:

        response=client.chat(
            model='qwen2.5-coder:7b',
            messages=[
                {
                    "role":"user",
                    "content":task
                }
            ]
        )

        print(
            "\nResponse:\n"
        )

        print(
            response["message"]["content"]
        )
