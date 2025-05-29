from random import random

import torch
import math

a = torch.tensor([3.5])
a = a.cpu()
b = a.numpy()
print(type(a),type(b))
print(b)

r = random()

print(r)