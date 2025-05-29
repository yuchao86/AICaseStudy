import chardet
import sys

print("开始检查文件编码...")
try:
    with open('../DeepSeek-V3/prompt_optimizer.py', 'rb') as f:
        print("成功打开文件")
        raw_data = f.read()
        print(f"读取了 {len(raw_data)} 字节数据")
        result = chardet.detect(raw_data)
        print(f"文件编码: {result['encoding']} (置信度: {result['confidence']})")
except Exception as e:
    print(f"发生错误: {str(e)}", file=sys.stderr)
