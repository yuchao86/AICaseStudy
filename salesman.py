from openai import OpenAI

client = OpenAI(
    base_url="https://api.deepseek.com/",
    api_key="sk-**"
)

completion = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {
                "role": "system",
                "content": "请你扮演一个有20年中小学K12在线教育的老师，并且有丰富的成功经验的销售，说话时候需要照顾客户的情绪价值，"
                           "显得非常有亲和力，对话中总是带有很强的同理心，理解学生客户的购买价值。"
        },
        {
                "role": "user",
                "content": "请问我数学成绩怎么从60分提高到90分以上，需要购买哪些课程。"
        }
    ]
)

print(completion.choices[0].message.content)