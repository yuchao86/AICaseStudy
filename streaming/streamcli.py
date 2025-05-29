import json
import requests

# url_api = "http://10.4.0.141:800h1/cat/stream"
url_api = "http://localhost:7777/api"


with requests.post(url_api, stream=True) as r:
    r.raise_for_status()  # 检查请求是否成功
    print(r.iter_lines())
    for line in r.iter_lines():
        if line:  # 过滤掉保持连接的空行
            print(json.loads(line.decode('utf-8')))
