from transformers import BertTokenizer
import torch
from transformers import BertModel


tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
model = BertModel.from_pretrained("bert-base-chinese")

encoded_input = tokenizer(
    "今天天气很好",
    padding="max_length",
    max_length=50,
    truncation=True,
    return_tensors="pt"
)

def predict(sentence):
    inputs = tokenizer(sentence, return_tensors="pt", padding="max_length", max_length=50, truncation=True)
    with torch.no_grad():
        logits = model(**inputs).squeeze()
    prob = torch.sigmoid(logits).item()
    return "完整" if prob > 0.5 else "不完整"

# 测试样例
print(predict("因为天气不好"))  # 不完整
print(predict("因为天气不好，所以取消了活动。"))  # 完整