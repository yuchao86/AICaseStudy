# region 加载库，先测试一把，并配置参数
import numpy as np
import gym

# 创建环境env
env = gym.make('CartPole-v0')

# 测试随机Action的表现
# 初始化环境
env.reset()
random_episodes = 0
reward_sum = 0
while random_episodes < 10:  # 玩10把
    # 渲染图像
    env.render()
    # 使用np.random.randint(0,2)产生随机的Action
    # env.step()执行这个而Action.
    observation, reward, done, _ = env.step(np.random.randint(0, 2))
    # 累加到这把的总奖励里
    reward_sum += reward
    # done为True,即任务失败,则实验结束
    if done:
        # 展示这次试验累计的奖励
        random_episodes += 1
        print("Reward for this episode was:", reward_sum)
        reward_sum = 0
        # 初始化环境
        env.reset()

# hyperparameters
H = 50  # 50个隐层神经元
batch_size = 25  # every how many episodes to do a param update?
learning_rate = 1e-1  # 学习速率
gamma = 0.99  # reward的discount比例，要＜１，防止reward被无损耗地不断累加导致发散．未来奖励不确定性必须打折
D = 4  # input dimensionality

# endregion


# endregion

# 用来估算每一个Action对应的潜在价值discount_r
def discount_rewards(r):
    """ take 1D float array of rewards and compute discounted reward """
    discounted_r = np.zeros_like(r)
    running_add = 0
    for t in reversed(range(r.size)):
        # r[0]就是gg时的动作价值,r[1]就是gg前的动作价值,最后的r[]才是本步的动作价值
        running_add = running_add * gamma + r[t]
        discounted_r[t] = running_add
    return discounted_r


# xs是环境信息observation的列表
# ys是人为定义的label列表
# drs是每一个Action的Reward
xs, ys, drs = [], [], []
reward_sum = 0  # 累计的reward
episode_number = 1
total_episodes = 10000  # 总的试验次数

# region 执行计算图

# endregion