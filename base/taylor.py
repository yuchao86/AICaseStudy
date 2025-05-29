import numpy as np
import matplotlib.pyplot as plt
import math

#定义计算泰勒级数展开的函数
def taylor_cos(x,terms):
    '''
    f(x)=cosx
    :param terms: 项数
    '''
    result=0
    for n in range(terms):
        coefficient=(-1)**n / math.factorial(2*n)
        result += coefficient * x ** (2*n)
    return  result

#生成x值
x_values=np.linspace(-2*np.pi,2*np.pi,100)
#计算不同项数的泰勒级数展开的近似值
approx_values_t7=[taylor_cos(x,7) for x in x_values]
approx_values_t5=[taylor_cos(x,5) for x in x_values]
approx_values_t10=[taylor_cos(x,10) for x in x_values]
approx_values_t100=[taylor_cos(x,100) for x in x_values]

#绘制图形
plt.figure(figsize=(8,6))
plt.plot(x_values,np.sin(x_values),label='cos(x)',color='b')
plt.plot(x_values,approx_values_t7,label='Talor Approximation T7',linestyle='--',color='r')
#plt.plot(x_values,approx_values_t5,label='Talor Approximation T5',linestyle='--',color='g')
#plt.plot(x_values,approx_values_t10,label='Talor Approximation T10',linestyle='--',color='y')
#plt.plot(x_values,approx_values_t100,label='Talor Approximation T100',linestyle='-',color='k')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.legend()
plt.grid(True)
plt.show()