import asyncio
import edge_tts

TEXT = """
浏览器本身也是通过EventSource这一个内置的API来接收这 流式SSE 的数据并处理。EventSource是一个用于服务器发送事件（Server-Sent Events, SSE）的浏览器API。允许网页从服务器接收自动更新的消息，而不需要客户端轮询。
不过这个EventSource有一个非常致命的缺点，那就是 只支持GET类型的请求，并且不支持任何自定义的头部."""
VOICE = "zh-GB-SoniaNeural"
OUTPUT_FILE = "test.mp3"


async def amain() -> None:
    """Main function"""
    communicate = edge_tts.Communicate(TEXT, VOICE)
    with open(OUTPUT_FILE, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                print(f"WordBoundary: {chunk}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    try:
        loop.run_until_complete(amain())
    finally:
        loop.close()