import sympy as sp
import matplotlib.pyplot as plt
from sympy.plotting import plot
from sympy import exp

# 定义一个符号变量
x = sp.symbols(' x')
y = sp.symbols(' y')

# 定义一个数学表达式
#expr = sp.exp(-x) * sp.sin(x)
#expr = sp.log(x,20)
expr = x - ( x ** 3)/3


# 使用SymPy的plot函数绘制表达式图形
p = plot(expr, (x, -5, 5), show=False, line_color='blue')
p[0].line_color = 'blue'  # 设置线条颜色为蓝色
p[0].label = r'$e^{-x}\sin(x)$'  # 设置图例标签为数学表达式

p.show()  # 显示图形窗口

#sp.plotting.plot3d(x*exp(-x**2-y**2), (x, -3, 3), (y, -2, 2))
