# import csv
import os
import time
# import random
# import torch.nn.functional as F
import torch
import numpy as np
from .trainer import Trainer
# from Visualize import Visualizer
from .datasets_npz import TrainDataset
from torch.autograd import Variable
from collections import OrderedDict
# from dwt import IWT
# from train_ab import Metric
from .save import save_one
# from save import save_one_as_jpg
from torch.utils.data import DataLoader

# 生成图像，并将生成的图像与真实图像进行对比保存。
torch.manual_seed(1337)
torch.cuda.manual_seed(1337)


def back(x):
    return x / 2 + 0.5


def generate_mha(folder_path):
    param = OrderedDict()
    # os.environ['CUDA_VISIBLE_DEVICES'] = '
    param['gpu_ids'] = [0]
    # vis = Visualizer('test150')
    path = folder_path
    # path = r"/home/byte/PycharmProjects/website/chart/resource/"
    # path = r"/home/user/data/lost+found/mha/UNET"
    # 检验路径
    # if not os.path.exists(path):
        # os.makedirs(path)
    # 设置GPU的可用
    torch.backends.cudnn.enabled = True
    torch.backends.cudnn.benchmark = True

    model = Trainer(gpu_ids=param['gpu_ids'], is_Train=True, continue_train=True)
    # model.load_state_dict(torch.load(r"/home/user/data/lost+found/unet/520_net.pth"))
    batch = 4  # dataloader的bs是1 但是由于数据是3D的 取出来时是1 1 185 6 512 512（其中第二个1是dataloader是人为误操作）
    # 我们人工设置batch=2得到2 6 512 512（其中2是依次取到185）来达到2D输入网络

    # 测试集合的路径
    # dir = r"/home/user/data/lost+found/lab_dataset/rectum333_npz/test"
    # dir = r"/home/byte/PycharmProjects/website/chart/resource/"
    test_dir = folder_path
    Syn_test = TrainDataset(test_dir)

    trainData = DataLoader(dataset=Syn_test, batch_size=1, shuffle=False, drop_last=True, num_workers=1)
    # print(len(trainData))
    if True:

        for ii, batch_sample in enumerate(trainData):

            inputs, target, channel, name = batch_sample['inputs'], batch_sample['rd'], \
                batch_sample['channel'], batch_sample['name'][0]
            print(name)

            inputs = inputs.squeeze(0)

            # 131：表示张量的第一个维度的大小，通常是批次大小，即这个张量包含了 131 个样本。
            # 6：表示张量的第二个维度的大小，通常是通道数或特征数量，即这个张量包含了 6 个通道或特征。
            # 160：表示张量的第三个维度的大小，通常是图像的高度，即每个图像有 160 个像素点高。
            # 160：表示张量的第四个维度的大小，通常是图像的宽度，即每个图像有 160 个像素点宽。

            target = target.squeeze(0)

            # print(c)
            crop = (channel % 32) // 2
            endd = (channel - crop) % 32
            start_slice = crop
            # start_slice=0  # 将输入和输出对齐
            inputs = inputs[start_slice:]
            target = target[start_slice:]
            # 创建了一个形状为 (channel, 160, 160) 的全零数组 fakes + reals，用于存储模型生成的假数据
            fakes = np.zeros(shape=(channel, 160, 160))
            reals = np.zeros(shape=(channel, 160, 160))
            epoch_start_time = time.time()

            for i in range((channel - start_slice) // batch):
                if batch * i + batch <= channel:  # 这样会少最后一个batch 所以改为<=c
                    # print(batch*i + batch)
                    main_inputs = inputs[batch * i:batch * (i + 1), :, :, :]  # main_inputs: [4 , 6, 160, 160]
                    main_target = target[batch * i:batch * (i + 1), :, :, :]
                    # main_target: [4 , 1, 160, 160]
                else:
                    break

                main_inputs, main_target = Variable(main_inputs).cuda(), Variable(main_target).cuda()

                with torch.no_grad():
                    model.forward(main_inputs, main_target)
                    # 相关的实现功能---见相关的代码
                    visuals = model.get_current_visuals(sample=True)
                    fake = back((visuals['SAM'])).clamp_(0., 1.).detach().cpu().numpy()
                    # vis.img("sam",fake)
                    tar = back(model.target).clamp_(0., 1.).detach().cpu().numpy()
                    fakes[start_slice + batch * i:start_slice + batch * i + batch, :,
                    :] = fake.squeeze()  # 1 512 512 的c不影响

                    reals[start_slice + batch * i:start_slice + batch * i + batch, :, :] = tar.squeeze()
            print(ii)
            save_one(fakes, reals, path, name)
            # save_one_as_jpg(fakes, reals, path, name)
