from openai import OpenAI

client = OpenAI(api_key='sk-proj-****')
completion = client.chat.completions.create(
    model="gpt-4o",
    store=True,
    messages=[
        {
                "role": "system",
                "content": "请你扮演一个有20年中小学K12在线教育的销售经理，并且有丰富的成单经验的王牌销售，说话时候需要照顾客户的情绪价值，"
                           "显得非常有亲和力，对话中总是带有很强的同理心，理解学生客户的购买价值。"
        },
        {
                "role": "user",
                "content": "请问我数学成绩怎么从60分提高到90分以上，需要购买哪些课程。"
        }
    ]
)
