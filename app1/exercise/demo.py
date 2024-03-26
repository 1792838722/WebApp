import torch.nn as nn
import torch
import torch.nn.functional as F
from torchvision.models import resnet50


class DoubleConv(nn.Module):
    """(convolution => [BN] => ReLU) * 2"""
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.double_conv = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True)
        )
    def forward(self, x):
        return self.double_conv(x)

class Down(nn.Module):
    """Downscaling with maxpool then double conv"""
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.maxpool_conv = nn.Sequential(
            nn.MaxPool2d(2),
            DoubleConv(in_channels, out_channels)
        )
    def forward(self, x):
        return self.maxpool_conv(x)

class Up(nn.Module):
    """Upscaling then double conv"""
    def __init__(self, in_channels, out_channels, bilinear=True):
        super().__init__()
        # if bilinear, use the normal convolutions to reduce the number of channels
        if bilinear:
            # self.up = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)
            self.up = nn.Sequential(nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True),
                                    nn.Conv2d(in_channels, in_channels // 2, kernel_size=3, padding=1),
                                    nn.ReLU(inplace=True))
        else:
            self.up = nn.ConvTranspose2d(in_channels, in_channels // 2, kernel_size=2, stride=2)
        self.conv = DoubleConv(in_channels, out_channels)
    def forward(self, x1, x2):
        x1 = self.up(x1)
        x = torch.cat([x2, x1], dim=1)
        return self.conv(x)

class OutConv(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(OutConv, self).__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size=1)
    def forward(self, x):
        return self.conv(x)


class UNet(nn.Module):
    def __init__(self, n_channels, n_classes, m=2,bilinear=True):
        super(UNet, self).__init__()
        self.n_channels = n_channels
        self.n_classes = n_classes
        self.bilinear = bilinear

        self.inc = DoubleConv(n_channels, 8*m)
        self.down1 = Down(8*m, 16*m)
        self.down2 = Down(16*m, 32*m)
        self.down3 = Down(32*m, 64*m)
        self.down4 = Down(64*m, 128*m)
        self.up1 = Up(128*m, 64*m, bilinear)
        self.up2 = Up(64*m, 32*m, bilinear)
        self.up3 = Up(32*m, 16*m, bilinear)
        self.up4 = Up(16*m, 8*m, bilinear)
        self.outc = OutConv(8*m, n_classes)

    def forward(self, x, target):
        x1 = self.inc(x)
        x2 = self.down1(x1)
        x3 = self.down2(x2)
        x4 = self.down3(x3)
        x5 = self.down4(x4)
        # print(x5.shape)
        # print(x4.shape)
        x = self.up1(x5, x4)
        x = self.up2(x, x3)
        x = self.up3(x, x2)
        x = self.up4(x, x1)
        logits = self.outc(x)
        # output = F.sigmoid(logits)
        return logits



if __name__ == '__main__':
    net = UNet(n_channels=6, n_classes=1)
    print(net)
    # for name, layer in net.named_modules():
    #     print(name)
    # down1.maxpool_conv.1.double_conv.3
    # down2.maxpool_conv.1.double_conv.3
    # down3.maxpool_conv.1.double_conv.3
    # down4.maxpool_conv.1.double_conv.3

    # model = resnet50(pretrained=False, num_classes=365)
    # print("-----------------------------------------------------")
    # for name, layer in model.named_modules():
    #     print(name)

