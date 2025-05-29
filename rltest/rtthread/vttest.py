
import time
import vthread
import time, random, queue
from vthread import pool, lock

#
# @vthread.pool(6) # 只用加这一行就能实现6条线程池的包装
# def foolfunc(num):
#     time.sleep(1)
#     print(f"foolstring, test2 foolnumb: {num}")
#
# for i in range(10):
#     foolfunc(i) # 加入装饰器后，这个函数变成往伺服线程队列里塞原函数的函数了
#
# # 不加装饰就是普通的单线程
# # 只用加一行就能不破坏原来的代码结构直接实现线程池操作，能进行参数传递
# #
# # 执行效果如下：
# # [  Thread-1_0 ] foolstring, test2 foolnumb: 0
# # [  Thread-3_0 ] foolstring, test2 foolnumb: 2
# # [  Thread-6_0 ] foolstring, test2 foolnumb: 5
# # [  Thread-2_0 ] foolstring, test2 foolnumb: 1
# # [  Thread-5_0 ] foolstring, test2 foolnumb: 4
# # [  Thread-4_0 ] foolstring, test2 foolnumb: 3
# # [  Thread-2_0 ] foolstring, test2 foolnumb: 9
# # [  Thread-3_0 ] foolstring, test2 foolnumb: 7
# # [  Thread-6_0 ] foolstring, test2 foolnumb: 8
# # [  Thread-1_0 ] foolstring, test2 foolnumb: 6
#
#
pool_1 = vthread.pool(5,gqueue=1) # 开5个伺服线程，组名为1
pool_2 = vthread.pool(2,gqueue=2) # 开2个伺服线程，组名为2

@pool_1
def foolfunc1(num):
    time.sleep(1)
    print(f"foolstring1, test3 foolnumb1:{num}")

@pool_2 # foolfunc2 和 foolfunc3 用gqueue=2的线程池
def foolfunc2(num):
    time.sleep(1)
    print(f"foolstring2, test3 foolnumb2:{num}")
@pool_2 # foolfunc2 和 foolfunc3 用gqueue=2的线程池
def foolfunc3(num):
    time.sleep(1)
    print(f"foolstring3, test3 foolnumb3:{num}")

for i in range(10): foolfunc1(i)
for i in range(10): foolfunc2(i)
for i in range(10): foolfunc3(i)
# # 额外开启线程池组的话最好不要用gqueue='v'
# # 因为gqueue='v'就是默认参数
#
#
# @vthread.pool(5)
# def foolfunc_():
#
#     @vthread.atom # 将函数加锁封装
#     def do_some_fool_thing1():
#         pass # do_something
#     @vthread.atom # 将函数加锁封装
#     def do_some_fool_thing2():
#         pass # do_something
#
#     # 执行时就会实现原子操作
#     do_some_fool_thing1()
#     do_some_fool_thing2()
#
#
# # 可以使用 vthread.pool.wait 函数来等待某一组线程池执行完毕再继续后面的操作
# # 该函数仅有一个默认参数 gqueue='v'，需要等待的分组。
# # 该函数的本质就是一个定时循环内部使用 vthread.pool.check_stop 函数不停检测某个任务组是否结束。
# # check_stop 函数返回结果为 0 则为线程池已执行结束。
# # 如果有比 wait 更丰富的处理请使用 check_stop 。
#
#
# @vthread.pool(10)
# def foolfunc_():
#     time.sleep(1)
#     print(123)
# for i in range(10): foolfunc_()
#
# vthread.pool.wait() # 等待gqueue='v'分组线程执行完毕再继续后面的代码
# # vthread.pool.waitall() # 当你的程序执行过程比较单调时，可以考虑等待全部线程池都执行完再往后继续。
# print('end.')


ls = queue.Queue()
producer = 'pr'
consumer = 'co'

@pool(6, gqueue=producer)
def creater(num):
    time.sleep(random.random()) # 随机睡眠 0.0 ~ 1.0 秒
    print("数据进入队列: {}".format(num))
    ls.put(num)
@pool(1, gqueue=consumer)
def coster():
    # 这里之所以使用 check_stop 是因为，这里需要边生产边消费
    while not pool.check_stop(gqueue=producer):
        time.sleep(random.random()) # 随机睡眠 0.0 ~ 1.0 秒
        pp = [ls.get() for _ in range(ls.qsize())]
        print('当前消费的列表 list: {}'.format(pp))

for i in range(30): creater(i)
coster() # 写作逻辑限制了这里的数量
pool.wait(gqueue=producer) # 等待默认的 gqueue=producer 组线程池全部停止再执行后面内容
pool.wait(gqueue=consumer) # 等待默认的 gqueue=consumer 组线程池全部停止再执行后面内容
print('当生产和消费的任务池数据都结束后，这里才会打印')
print('current queue size:{}'.format(ls.qsize()))
print('end')


ls1 = queue.Queue()
ls2 = queue.Queue()
producer = 'pr'
consumer1 = 'co1'
consumer2 = 'co2'

@pool(6, gqueue=producer)
def creater(num):
    time.sleep(random.random()) # 随机睡眠 0.0 ~ 1.0 秒
    num1, num2 = num, num*num+1000
    print("数据进入队列: num:{}".format(num))
    ls1.put(num1)
    ls2.put(num2)

# 两个消费者
@pool(1, gqueue=consumer1)
def coster1():
    while not pool.check_stop(gqueue=producer):
        time.sleep(random.random()) # 随机睡眠 0.0 ~ 1.0 秒
        pp = [ls1.get() for _ in range(ls1.qsize())]
        print('当前消费的列表 list: {}'.format(pp))
@pool(1, gqueue=consumer2)
def coster2():
    while not pool.check_stop(gqueue=producer):
        time.sleep(random.random()) # 随机睡眠 0.0 ~ 1.0 秒
        pp = [ls2.get() for _ in range(ls2.qsize())]
        print('当前消费的列表 list: {}'.format(pp))
for i in range(30): creater(i)
coster1()
coster2()

pool.waitall() # 当需要简单等待全部任务结束再执行某些任务时，这样处理即可，这个等于下面注释中的内容。
# pool.wait(gqueue=producer)
# pool.wait(gqueue=consumer1)
# pool.wait(gqueue=consumer2)
print('当生产和消费的任务池数据都结束后，这里才会打印')
print('current queue 1 size:{}'.format(ls1.qsize()))
print('current queue 2 size:{}'.format(ls2.qsize()))
print('end')