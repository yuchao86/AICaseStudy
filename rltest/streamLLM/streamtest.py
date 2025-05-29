import openai
from threading import Thread
import asyncio
from queue import Queue
import time
from latex2pinyin.api import ChineseCutter, ChineseCutterParams
import datetime as dt
import logging


class ChatAgent:
    PROMPT = '''你是校外辅导机构的课程顾问，你有丰富的成功的销售经验，说话时候需要照顾客户的情绪价值，显得非常有亲和力，
对话中总是带有很强的同理心

'''

    def __init__(self, user_session):
        self.system_prompt = {"role": "system", "content": self.PROMPT}
        self.start_chat = {"role": "assistant", "content": "你好，我是王老师。"}
        self.chat_history = [self.start_chat]
        # {"role": "assistant", "content": "你好，我是王老师，咱们前面微信上有过沟通，您给我说过孩子英语学科比较薄弱，我就一直放在心上，跟您打这个电话，主要是想了解下咱孩子的具体学习情况，看我这边能为孩子提供什么样的助力，整理一些知识点总结和适合他的学习资料，帮孩子把成绩提升上来，您看可以吧？"}
        self.llm = openai.OpenAI(base_url="http://10.43.0.168:8080/v1", api_key="xxx")
        self.sent_cutter = ChineseCutter(params=ChineseCutterParams())
        self.user_session = user_session
        # self.thread = Thread(target=self.tts_thread)
        # self.push_queue = Queue()
        # self.tts_task = None
        # self.thread.start()

    async def play_start(self):
        message = self.start_chat["content"]
        await self.async_tts(message)
        await self.user_session.async_chat(message)

    async def async_tts(self, message: str):
        try:
            from streamLLM.tts import yuai_tts as tts
            # from llm.tts import doubao_tts as tts

            logging.info("tts start")
            audio = tts(message)
            logging.info("tts end")
            await self.user_session.play_tts_audio(audio)
            logging.info("play end")
        except Exception as e:
            print(e)

    async def reply(self, message: str):
        self.chat_history.append({"role": "user", "content": message})
        if len(self.chat_history) > 30:
            self.chat_history.pop(0)

        start = time.time()
        response = self.llm.chat.completions.create(
            temperature=0.8,
            model="sxz_qwen25_14b",
            max_tokens=512,
            top_p=0.5,
            stream=True,
            messages=[self.system_prompt] + self.chat_history
        )
        tasks = []
        chunks, reply = [], []
        n = 1
        for chunk in response:
            chunk_time = time.time() - start
            chunks.append(chunk)
            reply.append(chunk.choices[0].delta.content)
            splits = self.sent_cutter.add(reply[-1])
            for split in splits:
                logging.info(f"Push Split:{split}")
                if len(tasks) > 0:
                    await tasks[-1]
                t = asyncio.create_task(self.async_tts(split.text))
                tasks.append(t)
                # self.do_tts(split.text)
                # self.push_queue.put(split)
            if chunk_time > n:
                print(f"Received chunk({reply}) in {chunk_time:.2f} seconds")
                n += 1

        logging.info(f"gen done, time:{time.time() - start}")
        for split in self.sent_cutter.close():
            logging.info(f"Push Split:{split}")
            if len(tasks) > 0:
                await tasks[-1]
            t = asyncio.create_task(self.async_tts(split.text))
            tasks.append(t)
            # self.do_tts(split.text)
            # self.push_queue.put(split)
        # 使用asyncio.gather等待所有TTS任务完成
        if len(tasks) > 0:
            logging.info(f"等待{len(tasks)}个TTS任务完成")
            await tasks[-1]
            logging.info("所有TTS任务已完成")

        reply = "".join(reply)
        logging.info(f"Reply:{reply}")
        self.chat_history.append({"role": "assistant", "content": reply})
        await self.user_session.async_chat(reply)

# if __name__ == "__main__":
#     agent = ChatAgent()
#     agent.play_start()