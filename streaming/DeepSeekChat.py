import requests
import json

class DeepSeekChat:
    def __init__(self, api_key, model="deepseek-chat"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.deepseek.com/v1/chat/completions"
        self.history = []  # 存储完整的对话历史

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def chat_stream(self, prompt):
        # 将用户输入加入历史
        self.history.append({"role": "user", "content": prompt})

        # 构造请求体
        payload = {
            "model": self.model,
            "messages": self.history,
            "stream": True
        }

        # 发送流式请求
        response = requests.post(
            self.base_url,
            headers=self._get_headers(),
            json=payload,
            stream=True
        )

        full_response = []
        print("\nAssistant: ", end="", flush=True)

        # 处理流式响应
        if response.status_code == 200:
            for chunk in response.iter_lines():
                if chunk:
                    decoded_chunk = chunk.decode('utf-8')
                    data = decoded_chunk.startswith("data: ")
                    if data != "[DONE]":
                        print(decoded_chunk[6:])
                        json_chunk = json.loads(decoded_chunk[6:])
                        if "content" in json_chunk["choices"][0]["delta"]:
                            content = json_chunk["choices"][0]["delta"]["content"]
                            print(content, end="", flush=True)
                            full_response.append(content)
        else:
            print(f"\n请求失败，状态码：{response.status_code}")
            print(response.text)
            return None

        # 将助手的完整响应加入历史
        self.history.append({
            "role": "assistant",
            "content": "".join(full_response)
        })

        return "".join(full_response)

if __name__ == "__main__":
    # 初始化时填入你的API Key
    api_key = "sk-***"
    chat = DeepSeekChat(api_key)

    print("开始对话（输入 'exit' 退出）")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        chat.chat_stream(user_input)

    print("\n完整对话历史：")
    for msg in chat.history:
        print(f"{msg['role'].capitalize()}: {msg['content']}")
