import os
import yaml

configFile = os.path.dirname(os.path.realpath(__file__))+"/app.yaml"

env = os.getenv('env')

sessionId = f"project-{env}.session-id"
def sessionId(): pass

print(sessionId)

# 方法1：使用safe_load()方法
with open("app.yaml", "r") as file:
    data = yaml.safe_load(file)

# 方法2：使用load()方法
with open("app.yaml", "r") as file:
    data = yaml.load(file, Loader=yaml.Loader)

# 方法3：使用load_all()方法读取多个yaml文档
with open("app.yaml", "r") as file:
    documents = yaml.load_all(file, Loader=yaml.Loader)
    print(type[documents])
    for doc in documents:
        print(doc['service']['app']['name'])
