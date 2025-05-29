import requests
import json
from datetime import datetime

DEEPSEEK_API_KEY = "sk-c303adc049024f8ea544b03d4a5f81a9"
API_ENDPOINT = "https://api.deepseek.com/v1/chat/completions"

conversation_history = []
log_file = "conversation.log"


def stream_chat(prompt):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    conversation_history.append({"role": "user", "content": prompt})

    data = {
        "model": "deepseek-chat",
        "messages": conversation_history,
        "stream": True,
        "temperature": 0.7,
        "max_tokens": 1000
    }

    response = requests.post(API_ENDPOINT, headers=headers, json=data, stream=True)

    full_response = ""
    for chunk in response.iter_lines():
        if chunk:
            decoded_chunk = chunk.decode('utf-8').replace('data: ', '')
            try:
                chunk_data = json.loads(decoded_chunk)
                content = chunk_data['choices'][0]['delta']['content']
                print(content, end='', flush=True)
                full_response += content
            except json.JSONDecodeError:
                pass

    conversation_history.append({"role": "assistant", "content": full_response})
    save_conversation(prompt, full_response)
    print("\n")


def save_conversation(question, answer):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] User: {question}\n")
        f.write(f"[{timestamp}] Assistant: {answer}\n\n")


# 示例调用
while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit']:
        break
    print("Assistant: ", end='')
    stream_chat(user_input)
