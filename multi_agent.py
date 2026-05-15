import ollama

client = ollama.Client(
    host='http://192.168.1.19:11434'
)

agents = {

"planner":
"""
You are Planner.
Break goals into steps.
""",

"coder":
"""
You are Coder.
Write implementation details.
""",

"critic":
"""
You are Critic.
Find flaws and risks.
"""
}

while True:

    task=input("\nTask: ")

    if task=="exit":
        break

    outputs={}

    for name,prompt in agents.items():

        response=client.chat(
            model='qwen2.5-coder:7b',
            messages=[
                {
                    "role":"system",
                    "content":prompt
                },
                {
                    "role":"user",
                    "content":task
                }
            ]
        )

        outputs[name]=response[
            "message"
        ]["content"]

    for k,v in outputs.items():

        print(
            f"\n[{k.upper()}]\n"
        )

        print(v)
