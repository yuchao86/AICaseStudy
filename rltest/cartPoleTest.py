

import gym
import random
import torch
import torch.nn as nn
from torch.utils.data import Dataset
env = gym.make('CartPole-v0')
#env = gym.make('MountainCar-v0') #action = (0,1,2) = (left, no_act, right)
#env = gym.make('Hopper-v3')

#print(env.action_space)
#print(env.observation_space)


def GetModel():
    #In features:4(state) ,out:2 action q
    return nn.Sequential(nn.Linear(4, 16), 
                         nn.LeakyReLU(inplace=True), 
                         #nn.BatchNorm1d(16),
                         nn.Linear(16,24),
                         nn.LeakyReLU(inplace=True), 
                         #nn.BatchNorm1d(24),
                         nn.Linear(24,2))

class RLDataset(Dataset):
    def __init__(self, samples, transform = None, target_transform = None):
        #samples = [(s,a,r,s_), ...]
        self.samples = self.transform(samples)
    def __getitem__(self, index):
        #if self.transform is not None:
        #    img = self.transform(img) 
        return self.samples[index]
    def __len__(self):
        return len(self.samples)
    def transform(self, samples):
        transSamples = []
        (s,a,r,s_) = samples[0]
        sT = None
        #aT = torch.zeros(1).float()
        #rT = torch.zeros(1).float()
        sT_ = None
        for (s,a,r,s_) in samples:
            sT = torch.tensor(s,).float()
            sT_ = torch.tensor(s_).float()
            transSamples.append((sT, a, r, sT_))
        return transSamples

def oneSideQ(s, a):
    q = 1
    if a == 0:
        q = 0
    return q

#for i in range(10):
#    print(env.action_space)

def GetSamplesFromEnv(env, model, epoch, max_steps, drop_ratio = 0.8):
    train_samples = []
    each_sample = None
    env.reset()
    observation_new = None
    observation_old = None
    model.eval()
    #inputT = torch.zeros((1,3))
    for i_episode in range(epoch):
        observation_new = env.reset()
        observation_old = env.reset()
        for t in range(max_steps):
            env.render()
            #print(observation)
            if random.random() > 1-drop_ratio:
                action = env.action_space.sample()
            else:
                inputT = torch.tensor(observation_new).float()
                #print(model(inputT))
                action = torch.argmax(model(inputT)).item()
                #print(action)
            observation_new, reward, done, info = env.step(action)
            #print(reward)
            #We record samples.
            if t > 0 :
                #each_sample = (observation_old, action-1, reward, observation_new, done)
                #reward += observation_new[0]

                if done:
                    reward -= 10
                each_sample = (observation_old, action, reward, observation_new)
                train_samples.append(each_sample)

            observation_old = observation_new

            if done:
                print("Episode finished after {} timesteps".format(t+1))
                break
    return train_samples




def TrainNet(net_target, net_eval, trainloader, criterion, optimizer, device, epoch_total, gamma):
    running_loss = 0.0
    iter_times = 0
    net_target.eval()
    net_eval.train()
    #change_lr_flag = False
    for epoch in range(epoch_total + 1):
        #change_lr_flag = False
        if epoch > 0:           
            print('epoch %d, loss %.5f' % (epoch, running_loss))
        running_loss = 0.0
        if epoch == epoch_total: #or iter_times > 64000:
            break
        
        # data = (state, action, 
        for i, data in enumerate(trainloader, 0):
            if iter_times % 100 == 0:
                net_target.load_state_dict(net_eval.state_dict())
            s,a,r,s_ = data
            optimizer.zero_grad()


            #output = Q_predicted.
            q_t0 = net_eval(s)
            q_t1 = net_target(s_).detach()
            q_t1 = gamma * (r + torch.max(q_t1,dim=1)[0])
          
            loss = criterion(q_t1, torch.gather(q_t0, dim=1, index=a.unsqueeze(1)).squeeze(1))
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
            iter_times += 1
    net_target.load_state_dict(net_eval.state_dict())    
    print('Finished Training')



device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
net_target, net_eval = GetModel(), GetModel()


criterion = nn.MSELoss()
optimizer = torch.optim.Adam(net_eval.parameters(),lr=0.01)
train_samples = []

PATH = 'cartpole_model/goodmodel30.pth'
net_eval.load_state_dict(torch.load(PATH))
net_target.load_state_dict(torch.load(PATH))
GetSamplesFromEnv(env,net_eval, 100, 200, 0)
pass
goodmodel_idx = 0
for i in range(31, 300):
    drop_ratio = 0.8-0.77*i
    sample_times = 10
    tmpSample = GetSamplesFromEnv(env,net_eval, sample_times, 200, drop_ratio)
    train_samples += tmpSample
    if len(tmpSample) > sample_times * 180:
        print("good model!save it!")
        torch.save(net_eval.state_dict(), "cartpole_model/goodmodel" + str(goodmodel_idx) + ".pth")
        goodmodel_idx += 1
    if len(train_samples) > 4000:
        train_samples = train_samples[len(tmpSample):len(train_samples)]
    trainset = RLDataset(train_samples)
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=64, shuffle=True, num_workers=0,pin_memory=True)
    TrainNet(net_target, net_eval, trainloader, criterion, optimizer, device, 30, 0.9)
    PATH = "cartpole_model/model"+str(i)+".pth"
    torch.save(net_eval.state_dict(), PATH)


env.close()

