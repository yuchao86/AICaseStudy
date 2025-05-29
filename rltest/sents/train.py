import torch.optim as optim
import torch.nn as nn
from transformers import BertClassifier
dataloader = []

# 初始化模型、优化器、损失函数
model = BertClassifier()
optimizer = optim.AdamW(model.parameters(), lr=2e-5)
criterion = nn.BCEWithLogitsLoss()

# 训练循环
for epoch in range(10):
    for batch in dataloader:
        input_ids = batch["input_ids"]
        attention_mask = batch["attention_mask"]
        labels = batch["labels"].float()

        outputs = model(input_ids, attention_mask).squeeze()
        loss = criterion(outputs, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()