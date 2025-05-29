from transformers import BertTokenizer, BertModel
import torch


# 初始化分词器和模型
tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
model = BertModel.from_pretrained('bert-base-chinese')

# 准备文本并编码
text = "我爱北京天安门"
inputs = tokenizer(text, return_tensors="pt")

# 使用模型进行编码并获取输出
with torch.no_grad():
    outputs = model(**inputs)
    last_hidden_states = outputs.last_hidden_state
    cls_token_embeddings = last_hidden_states[:, 0, :]  # 获取[CLS] token的嵌入
    print("CLS Token Embeddings:", cls_token_embeddings)

