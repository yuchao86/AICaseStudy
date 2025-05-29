from RealtimeTTS import TextToAudioStream, SystemEngine, AzureEngine, ElevenlabsEngine

engine = AzureEngine() # replace with your TTS engine
stream = TextToAudioStream(engine)
stream.feed("浏览器本身也是通过EventSource这一个内置的API来接收这 流式SSE 的数据并处理。EventSource是一个用于服务器发送事件（Server-Sent Events, SSE）的浏览器API。允许网页从服务器接收自动更新的消息，而不需要客户端轮询。不过这个EventSource有一个非常致命的缺点，那就是 只支持GET类型的请求，并且不支持任何自定义的头部.")
stream.play_async()