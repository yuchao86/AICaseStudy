from fastapi import FastAPI
import uvicorn
import os
import json
from starlette.responses import StreamingResponse
# from fastapi.responses import StreamingResponse
from transformers import TextIteratorStreamer
from threading import Thread
from modelscope import AutoModelForCausalLM, AutoTokenizer

# 创建一个FastAPI应用程序实例
app = FastAPI()

model_name = "gongjy/MiniMind2"

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    #device_map="auto",
    trust_remote_code=True,
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

prompt = "写一篇800字的作文,主题是关于英雄的爱国主义教育思想的作文"
messages = [
    {"role": "system", "content": "你是一个经验丰富的高中语文老师，辅导过多年的高三语文备考学生，作文方面尤其精通."},
    {"role": "user", "content": prompt}
]
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)
model_inputs = tokenizer([text], return_tensors="pt").to(model.device)


@app.post("/api")
def aaa():
    # StreamingResponse包装的是可迭代对象
    return StreamingResponse(handle_post_request())


def handle_post_request():
    # TextIteratorStreamer为异步。skip_prompt=True, skip_special_tokens=True可以去除输出中的|im_start|等标记
    streamer = TextIteratorStreamer(tokenizer, timeout=60.0, skip_prompt=True, skip_special_tokens=True)
    generation_kwargs = {
        "max_new_tokens": 1024,  # 或者任何其他生成参数
        "streamer": streamer,
    }
    thread = Thread(target=model.generate, kwargs={**model_inputs, **generation_kwargs})
    thread.start()

    answer = ''
    for new_text in streamer:
        answer += new_text
        print(answer)
        yield json.dumps({'content': answer}) + '\n'


if __name__ == "__main__":
    handle_post_request()
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("API_PORT", 7777)), workers=1)
