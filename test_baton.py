import ollama

client = ollama.Client(
    host='http://192.168.1.19:11434'
)

response = client.chat(
    model='qwen2.5-coder:7b',
    messages=[
        {
            'role': 'user',
            'content': 'Explain your role in Baton in one sentence.'
        }
    ]
)

print(response['message']['content'])
