import random
import time
import torch
import numpy as np
from trainer import Trainer
from Visualize import Visualizer    # 从Visualize中导入可视化工具
from datasets_npz import make_datasetS  # 加载数据集的dataloader，便于后期的预处理
from torch.autograd import Variable     # 一种自动计算梯度的机制，用于构建动态计算图。
from collections import OrderedDict     # 普通字典不同，OrderedDict 在迭代时会按照元素插入的顺序返回键值对。这对于需要保持元素顺序的场景非常有用

# 一个医学图像处理模型的训练脚本，用于训练生成对抗网络（GAN）模型。
def back(x):
    return x/2+0.5
# 初始化三个属性 sum、cnt、cur，分别表示累计和、计数和当前值。简单的指标记录方式
class Metric():
    def __init__(self):
        self.sum = 0
        self.cnt = 0
        self.cur = 0

    def add(self, x):
        self.sum += x
        self.cnt += 1



        self.cur = x

    def get_sum(self):
        return self.sum

    def get_avg(self):
        if self.cnt > 0:
            return self.sum/self.cnt
        else:
            return 0

    def clear(self):
        self.sum=0
        self.cnt=0
        self.cur=0

if __name__ == '__main__':
    param = OrderedDict()  # 初始化一个有序字典
    param['gpu_ids'] = [0]  # 设置使用的GPU的编号
    vis = Visualizer('U_net')  # 用于在训练过程中可视化模型的中间结果、损失曲线等信息
    torch.backends.cudnn.enabled = True
    torch.backends.cudnn.benchmark = True  # 启用 cuDNN 加速和优化的功能

    # 实例化一个可以加载数据集的对象，用于处理批数据
    trainData = make_datasetS()

    # 构建一个用于训练的模型
    model = Trainer(gpu_ids=param['gpu_ids'], is_Train=True, continue_train=True)
    batch = 2
    # 开始训练并更新学习率
    for epoch in range(295, 700):    # 循环遍历训练的 epochs，从 295 开始一直到 1000。

        loss_l = Metric()   # 低剂量
        loss_h = Metric()   # 高剂量
        loss = Metric()     # 总损失
        epoch_start_time = time.time()  # 记录每一步的训练开始时间

        for ii, batch_sample in enumerate(trainData):
            # 在这一个批次的信息之中获取输入数据+目标数据+通道数+名称
            inputs, target, channel, name = batch_sample['inputs'], batch_sample['rd'],\
                                              batch_sample['channel'], batch_sample['name']
            # 删除第一个维度
            inputs = inputs.squeeze(0)
            target = target.squeeze(0)

            # 随机决定从哪个切片开始处理
            start_slice = random.randint(0, batch - 1)
            inputs = inputs[start_slice:]
            target = target[start_slice:]

            # 遍历了从输入数据（inputs）和目标数据（target）中切片得到的数据。
            for i in range(((channel - start_slice) // batch)):
                # 批处理
                main_inputs = inputs[batch * i:batch * (i + 1), :, :, :]
                main_target = target[batch * i:batch * (i + 1), :, :, :]
                # 获取的数据转换为PyTorch的Variable对象，并将其移动到GPU上
                main_inputs, main_target = Variable(main_inputs).cuda(), Variable(main_target).cuda()
                # 模型的参数优化
                model.optimizer_parameters(main_inputs, main_target)

                prediction = model.forward(main_inputs,main_target)
                dose = torch.clamp(prediction,0.0,1.0)
                # print(dose)

                dose_show = dose.detach().cpu().numpy()  # 如果去掉detach 报错：loss.cpu().numpy())#报错 RuntimeError: Can't call numpy() on Variable that requires grad. Use var.detach().numpy() instead.
                target_show = back(model.target).detach().cpu().numpy()
                # np.savez(f'F:\\result\\dose{i}.npz',target_show=dose_show)
                
                vis.img("pre", img_=dose_show)
                vis.img("target", img_=target_show)
                vis.img("init", img_=back(model.pre).clamp(0., 1.).detach().cpu().numpy())
                loss_h.add(model.loss)
                loss.add(model.loss)
                # print(((channel - start_slice) // batch))

            print(1)
        vis.plot("loss_h", loss_h.get_avg().item())
        vis.plot("loss", loss.get_avg().item())
        # 累积损失清零
        loss_l.clear()
        loss_h.clear()
        loss.clear()
        epoch_end_time = time.time()  # 记录这一步的结束时间
        print('time consuming:', (epoch_end_time - epoch_start_time) / 60)
        print("local time", time.strftime('%c'))  # 本地时间
        # if epoch == 0 or epoch >= 30:
        print('save_model....')
        print('epoch: %d' % epoch)
        # 如果当前 epoch 的倍数是 50，就保存该 epoch 的模型
        if (epoch) % 20 == 0:
            model.save_model(epoch)
        model.save_model('latest')
