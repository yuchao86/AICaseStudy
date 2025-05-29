from pydub import AudioSegment
import numpy as np


def detect_vad(audio_file, silence_threshold=-50.0, min_silence_len=500):
    audio = AudioSegment.from_file(audio_file)
    # 转换音频数据为numpy数组
    samples = np.array(audio.get_array_of_samples())

    # 计算音频的能量
    energy = np.log10(np.abs(samples) + 1e-10)
    detected_segments = []
    segment_start = None

    for i in range(len(energy)):
        if energy[i] > silence_threshold:
            if segment_start is None:
                segment_start = i
        else:
            if segment_start is not None and (i - segment_start) > min_silence_len:
                detected_segments.append((segment_start, i))
                segment_start = None

    return detected_segments


# 使用示例
segments = detect_vad('n2pid-1wro9.wav', -5.0, 5)
for start, end in segments:
    print(f"Detected segment: Start={start}, End={end}")