# 导入所需的库
import sounddevice as sd
import soundfile as sf

# 定义测试麦克风的函数
def test_microphone(device_index=None, output_filename="output.wav"):
    # 设置录音参数
    duration = 5  # 录音时长（秒）
    fs = 44100  # 采样频率

    # 获取麦克风列表
    devices = sd.query_devices()
    # 如果提供了设备索引并且有效，则使用指定的麦克风
    if device_index is not None and device_index < len(devices):
        print(f"Using microphone: {devices[device_index]['name']}")
    else:
        print("Using default microphone.")

    # 获取并设置麦克风支持的采样率
    supported_rates = devices[device_index]['default_samplerate']
    if supported_rates != fs:
        print(f"Adjusting sample rate to {int(supported_rates)} Hz (supported by the device).")
        fs = int(supported_rates)  # 确保采样率是整数

    print("Recording...")
    # 使用sounddevice录制声音
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, device=device_index)

    # 等待录音完成
    sd.wait()

    print("Recording finished.")

    # 保存录音为WAV文件
    sf.write(output_filename, recording, fs)

    print(f"File saved as {output_filename}")

# 主函数入口
if __name__ == "__main__":
    # 获取麦克风列表并打印
    devices = sd.query_devices()
    for i, device in enumerate(devices):
        print(f"{i}: {device['name']}")

    # 用户输入选择麦克风设备索引
    device_index = int(input("Enter the index of the microphone to use: "))
    test_microphone(device_index)
