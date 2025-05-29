import math
import numpy as np
import matplotlib.pyplot as plt

# set x's range
x = np.arange(-10, 10, 0.1)
y1 = 1 / (1 + math.e ** (-x))  # sigmoid
# y11=math.e**(-x)/((1+math.e**(-x))**2)
y11 = 1 / (2 + math.e ** (-x)+ math.e ** (x))  # sigmoid的导数
y2 = (math.e ** (x) - math.e ** (-x)) / (math.e ** (x) + math.e ** (-x))  # tanh
y22 = 1-y2*y2  # tanh函数的导数
y3 = np.where(x < 0, 0, x)  # relu
y33 = np.where(x < 0, 0, 1)  # ReLU函数导数
plt.xlim(-4, 4)
plt.ylim(-1, 1.2)
ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.spines['bottom'].set_position(('data', 0))
ax.spines['left'].set_position(('data', 0))

# Draw pic
#plt.plot(x, y1, label='Sigmoid', linestyle="-", color="black")
#plt.plot(x, y11, label='Sigmoid derivative', linestyle="-", color="blue")

#plt.plot(x, y2, label='Tanh', linestyle="-", color="black")
#plt.plot(x, y22, label='Tanh derivative', linestyle="-", color="blue")

plt.plot(x, y3, label='Tanh', linestyle="-", color="black")
plt.plot(x, y33, label='Tanh derivative', linestyle="-", color="blue")

# Title
plt.legend(['Sigmoid', 'Tanh', 'Relu'])
#plt.legend(['Sigmoid', 'Sigmoid derivative'])  # y1 y11
#plt.legend(['Tanh', 'Tanh derivative'])  # y2 y22
plt.legend(['Relu', 'Relu derivative'])  # y3 y33

#plt.legend(['Sigmoid', 'Sigmoid derivative', 'Relu', 'Relu derivative', 'Tanh', 'Tanh derivative'])  # y3 y33
# plt.legend(loc='upper left')  # 将图例放在左上角

# save pic
# plt.savefig('plot_test.png', dpi=100)
plt.savefig(r"./")

# show it!!
plt.show()