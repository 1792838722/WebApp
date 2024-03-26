import os
import torch
import torch.nn as nn
import torch.nn.functional as F
from demo import UNet
from collections import OrderedDict


# from network.unet import UNet
# from network.deeplabv3_plus import DeepLabv3_plus
# from U_ResNet_D import U_ResNet_D
# from network.prunet import PRUNET, TotalLoss
# from network.u2net import U2NETP2_PSA_DA
# from network.transunet.transu import construct_transunet
# from network.dptrans.dptrans_builder import construct_dptrans
# from network.res_unet import UNet

class Trainer(nn.Module):
    def __init__(self, gpu_ids=[], is_Train=True, continue_train=True):
        super(Trainer, self).__init__()
        self.isTrain = is_Train
        self.gpu_ids = gpu_ids
        self.continue_train = continue_train
        self.sigmoid = nn.Sigmoid()
        # self.net =U_ResNet_D(7,1)
        # self.net = UNet(7,1,2)
        # self.net = DeepLabv3_plus(7,1)
        # self.net = PRUNET()
        # self.prunet_loss = TotalLoss().cuda()
        # self.net=U_ResNet_D(7,1)
        # self.net = construct_transunet()
        # self.net = U2NETP2_PSA_DA(7,1)
        # self.net = construct_dptrans()
        self.net = UNet(6, 1)

        if len(gpu_ids) > 0:
            assert (torch.cuda.is_available())
            self.net.cuda(gpu_ids[0])

        if self.isTrain:
            self.lr = 3e-5
            self.criterionL1 = nn.L1Loss()

            self.optimizer = torch.optim.Adam(self.net.parameters(), lr=self.lr, betas=(0.9, 0.999))

        if not self.isTrain or self.continue_train:
            print('----------load model-------------')

            # dir = r"/home/user/data/lost+found/unet/300_net.pth"
            dir = r"C:/Users/17928/Desktop/exercise/520_net.pth"
            self.net.load_state_dict(torch.load(dir), strict=False)

    def feed_data(self, data):
        # self.data = self.set_device(data)
        self.data = data

    def forward(self, input, target=None):
        self.input = input
        # self.input = F.avg_pool2d(input, kernel_size=6)  # 在通道维度上进行平均池化，将 6 个通道压缩成 1 个通道
        self.target = target
        # 报错
        result = self.net(self.input, torch.full((self.input.shape[0],), 0, device='cuda'))
        self.pre = f_enc = feats = result  # 解包前三个值

        self.data = {'HR': self.input, 'SR': torch.tensor(0), 'LF': f_enc, 'MF': feats}
        return self.pre

    def optimizer_parameters(self, input, target):
        self.net.zero_grad()

        self.forward(input, target)

        self.loss = self.criterionL1(self.pre, self.target)
        self.loss.backward()
        self.optimizer.step()

    def save_model(self, epoch):
        save_dir = r'F:\unet'
        # save_dir = r"/home/user/data/lost+found/unet"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        net_name = '%s_net.pth' % epoch
        net = os.path.join(save_dir, net_name)
        torch.save(self.net.cpu().state_dict(), net)
        self.net.cuda(self.gpu_ids[0])

    def get_current_visuals(self, need_LR=True, sample=False):
        out_dict = OrderedDict()
        if sample:
            out_dict['SAM'] = self.pre.detach().float().cpu()
        else:
            out_dict['SR'] = self.pre.detach().float().cpu()  # 使用模型输出作为超分辨率图像
            out_dict['INF'] = self.data['SR'].detach().float().cpu()
            out_dict['HR'] = self.data['HR'].detach().float().cpu()
            if need_LR and 'LR' in self.data:
                out_dict['LR'] = self.data['LR'].detach().float().cpu()
            else:
                out_dict['LR'] = out_dict['INF']
        return out_dict
