import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from collections import deque
import random

# 环境参数
STATE_DIM = 4  # 状态维度: [时间, 人数, 菜品, 确认状态]
ACTION_DIM = 3  # 动作: 0-询问时间, 1-询问人数, 2-确认订单
EPISODES = 500
MAX_STEPS = 10

# 设备配置
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# 1. MRF势函数网络
class MRFNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(STATE_DIM * 2, 16),
            nn.ReLU(),
            nn.Linear(16, 1)
        )

    def forward(self, s_prev, s_current):
        """计算相邻状态的势函数值"""
        combined = torch.cat([s_prev, s_current], dim=-1)
        return self.fc(combined)


# 2. 策略网络
class PolicyNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(STATE_DIM, 32),
            nn.Tanh(),
            nn.Linear(32, ACTION_DIM)
        )

    def forward(self, state):
        return torch.softmax(self.fc(state), dim=-1)


# 3. 对话环境模拟器
class RestaurantEnv:
    def __init__(self):
        self.goal = {
            'time': np.random.randint(18, 21),
            'people': np.random.randint(2, 5)
        }
        self.reset()

    def reset(self):
        self.state = [0, 0, 0, 0]  # [时间, 人数, 菜品, 确认状态]
        self.dialogue = []
        return self.state

    def step(self, action):
        done = False
        reward = 0

        # 用户模拟响应逻辑
        if action == 0:  # 询问时间
            self.state[0] = self.goal['time']  # 用户提供正确时间
            self.dialogue.append("System: 您想几点用餐？ User: {}点".format(self.goal['time']))
        elif action == 1:  # 询问人数
            self.state[1] = self.goal['people']
            self.dialogue.append("System: 有几位用餐？ User: {}位".format(self.goal['people']))
        elif action == 2:  # 确认订单
            if self.state[0] > 0 and self.state[1] > 0:
                self.state[3] = 1  # 确认成功
                reward += 10
                done = True
                self.dialogue.append("System: 订单已确认！")
            else:
                reward -= 2  # 未完成必要信息

        # 任务奖励
        task_reward = 1 if self.state[3] == 1 else 0

        return np.array(self.state), reward + task_reward, done, {}


# 4. 经验回放缓存
class ReplayBuffer:
    def __init__(self, capacity):
        self.buffer = deque(maxlen=capacity)

    def add(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        return random.sample(self.buffer, batch_size)

    def __len__(self):
        return len(self.buffer)


# 5. PPO Agent
class PPOMRFAgent:
    def __init__(self):
        self.policy = PolicyNetwork().to(device)
        self.mrf = MRFNetwork().to(device)
        self.optimizer = optim.Adam([
            {'params': self.policy.parameters(), 'lr': 1e-3},
            {'params': self.mrf.parameters(), 'lr': 1e-4}
        ])
        self.buffer = ReplayBuffer(10000)
        self.gamma = 0.99
        self.clip_epsilon = 0.2

    def get_action(self, state):
        state_tensor = torch.FloatTensor(state).to(device)
        probs = self.policy(state_tensor)
        dist = torch.distributions.Categorical(probs)
        action = dist.sample()
        return action.item(), dist.log_prob(action)

    def compute_mrf_reward(self, prev_state, current_state):
        """计算MRF连贯性奖励"""
        with torch.no_grad():
            prev_tensor = torch.FloatTensor(prev_state).to(device)
            current_tensor = torch.FloatTensor(current_state).to(device)
            mrf_score = self.mrf(prev_tensor, current_tensor).sigmoid()
        return mrf_score.item()

    def update(self):
        if len(self.buffer) < 32: return

        # 采样批量数据
        states, actions, rewards, next_states, dones = zip(*self.buffer.sample(32))

        # 转换为张量
        states = torch.FloatTensor(np.array(states)).to(device)
        actions = torch.LongTensor(actions).to(device)
        rewards = torch.FloatTensor(rewards).to(device)

        # 计算优势函数
        with torch.no_grad():
            old_probs = self.policy(states)
            old_dist = torch.distributions.Categorical(old_probs)
            old_log_probs = old_dist.log_prob(actions)

        # PPO损失计算
        new_probs = self.policy(states)
        new_dist = torch.distributions.Categorical(new_probs)
        new_log_probs = new_dist.log_prob(actions)

        ratio = (new_log_probs - old_log_probs).exp()
        clipped_ratio = torch.clamp(ratio, 1 - self.clip_epsilon, 1 + self.clip_epsilon)

        # MRF奖励计算
        mrf_rewards = []
        for i in range(1, len(states)):
            mrf_rewards.append(self.compute_mrf_reward(states[i - 1], states[i]))
        mrf_rewards = torch.FloatTensor([0] + mrf_rewards).to(device)

        total_rewards = rewards + 0.3 * mrf_rewards  # 综合奖励

        # 损失函数
        loss = -torch.min(ratio * total_rewards, clipped_ratio * total_rewards).mean()

        # 反向传播
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()


# 6. 训练流程
def train():
    env = RestaurantEnv()
    agent = PPOMRFAgent()

    for episode in range(EPISODES):
        state = env.reset()
        episode_reward = 0
        prev_state = None

        for step in range(MAX_STEPS):
            # 选择动作
            action, log_prob = agent.get_action(state)

            # 执行动作
            next_state, reward, done, _ = env.step(action)

            # 添加MRF奖励
            if prev_state is not None:
                mrf_reward = agent.compute_mrf_reward(prev_state, state)
                reward += 0.3 * mrf_reward

            # 存储经验
            agent.buffer.add(state, action, reward, next_state, done)

            # 更新状态
            state = next_state
            episode_reward += reward
            prev_state = state.copy()

            if done:
                break

        # 策略更新
        agent.update()

        # 每50轮打印日志
        if episode % 50 == 0:
            print(f"Episode {episode}, Reward: {episode_reward:.1f}")


# 7. 测试函数
def mytest(agent, num_episodes=10):
    success = 0
    for _ in range(num_episodes):
        env = RestaurantEnv()
        state = env.reset()
        done = False
        for _ in range(MAX_STEPS):
            action, _ = agent.get_action(state)
            next_state, _, done, _ = env.step(action)
            state = next_state
            if done:
                success += 1
                break
    print(f"Success Rate: {success / num_episodes * 100:.1f}%")


# 运行训练和测试
if __name__ == "__main__":
    # 训练模型
    train()

    # 加载训练好的Agent测试
    trained_agent = PPOMRFAgent()
    # 此处应加载保存的模型权重
    # trained_agent.policy.load_state_dict(torch.load('policy.pth'))

    # 测试性能
    mytest(trained_agent)