import numpy as np
import sounddevice as sd

from funasr import AutoModel

chunk_size = [0, 10, 5]     # [0, 10, 5] 600ms, [0, 8, 4] 480ms
encoder_chunk_look_back = 4 # number of chunks to lookback for encoder self-attention
decoder_chunk_look_back = 1 # number of encoder chunks to lookback for decoder cross-attention

model = AutoModel(model="paraformer-zh-streaming")

chunk_stride = chunk_size[1] * 960 # 600ms
buffer = None                      # 麦克风数据缓存
cache = {}                         # FunASR缓存

def callback(indata, frames, time, status):
	global buffer, cache
	if buffer is None:
		buffer = indata
	else:
		buffer = np.append(buffer, indata)
	if len(buffer) < chunk_stride * 3:
		return
	chunk = np.array([buffer[i] for i in range(0, chunk_stride * 3) if i % 3 == 0])
	res = model.generate(
		input=chunk,
		cache=cache,
		is_final=False,
		chunk_size=chunk_size,
		encoder_chunk_look_back=encoder_chunk_look_back,
		decoder_chunk_look_back=decoder_chunk_look_back,
	)
	print(res)
	buffer = buffer[chunk_stride * 3:]

with sd.InputStream(device=1, samplerate=48000, callback=callback):
	sd.sleep(5*60000) # 1分钟