import os
import json
import time
import requests
from datetime import datetime


def save_to_file(file, content, is_question=False):
    """保存对话内容到文件"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if is_question:
        file.write(f"\n[{timestamp}] Question:\n{content}\n\n[{timestamp}] Answer:\n")
    else:
        file.write(content)


def main():
    # 配置
    url = "https://api.siliconflow.cn/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_API_KEY"  # 替换为你的 API Key
    }

    # 打开文件用于保存对话
    with open("conversation.txt", "a", encoding="utf-8") as file:
        while True:
            # 获取用户输入
            question = input("\n请输入您的问题 (输入 q 退出): ").strip()

            if question.lower() == 'q':
                print("程序已退出")
                break

            # 保存问题
            save_to_file(file, question, is_question=True)

            # 准备请求数据
            data = {
                "model": "deepseek-ai/DeepSeek-V3",
                "messages": [
                    {
                        "role": "user",
                        "content": question
                    }
                ],
                "stream": True,
                "max_tokens": 2048,
                "temperature": 0.7,
                "top_p": 0.7,
                "top_k": 50,
                "frequency_penalty": 0.5,
                "n": 1,
                "response_format": {
                    "type": "text"
                }
            }

            try:
                # 发送流式请求
                response = requests.post(url, json=data, headers=headers, stream=True)
                response.raise_for_status()  # 检查响应状态

                # 处理流式响应
                for line in response.iter_lines():
                    if line:
                        line = line.decode('utf-8')
                        if line.startswith('data: '):
                            if line == 'data: [DONE]':
                                continue

                            try:
                                content = json.loads(line[6:])  # 去掉 'data: ' 前缀
                                if content['choices'][0]['delta'].get('content'):
                                    chunk = content['choices'][0]['delta']['content']
                                    print(chunk, end='', flush=True)
                                    file.write(chunk)
                                    file.flush()
                            except json.JSONDecodeError:
                                continue

                # 添加分隔符
                print("\n----------------------------------------")
                file.write("\n----------------------------------------\n")
                file.flush()

            except requests.RequestException as e:
                error_msg = f"请求错误: {str(e)}\n"
                print(error_msg)
                file.write(error_msg)
                file.flush()


if __name__ == "__main__":
    main()
