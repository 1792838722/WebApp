import SimpleITK as sit
import numpy as np
import os
# from record import comparison
def save_one(pre,real,path,name):
    pre[real==0]=0
    # 使用了 SimpleITK 库来创建一个图像对象 sit.Image，并将一个 NumPy 数组 pre 转换为该图像对象。
    fakes: sit.Image = sit.GetImageFromArray(pre)
    fakes.SetSpacing(spacing=(3, 3, 3))
    # 创建一个 SimpleITK 图像文件写入器对象 s，用于将图像保存到文件
    s = sit.ImageFileWriter()

    s.SetFileName(path + '/' + name+ '_pre.mha')
    s.Execute(fakes)
    sit.WriteImage(fakes, path + '/' +name+ '_pre.mha')

    reals: sit.Image = sit.GetImageFromArray(real)
    reals.SetSpacing(spacing=(3, 3, 3))
    s = sit.ImageFileWriter()
    s.SetFileName(path + '/' + name+ '_tar.mha')
    s.Execute(reals)
    sit.WriteImage(reals, path + '/' + name+ '_tar.mha')



def save_one_as_jpg(pre, real, path, name):
    pre[real == 0] = 0

    # 保存预测结果的每个切片为JPG文件
    for i in range(pre.shape[0]):
        slice_pre = pre[i, :, :]
        slice_pre = sit.GetImageFromArray(slice_pre)
        slice_pre.SetSpacing(spacing=(3, 3))
        slice_pre = sit.Cast(slice_pre, sit.sitkUInt8)
        sit.WriteImage(slice_pre, os.path.join(path, f"{name}_pre_slice_{i}.jpg"))

    # 保存真实结果的每个切片为JPG文件
    for i in range(real.shape[0]):
        slice_real = real[i, :, :]
        slice_real = sit.GetImageFromArray(slice_real)
        slice_real.SetSpacing(spacing=(3, 3))
        slice_real = sit.Cast(slice_real, sit.sitkUInt8)
        sit.WriteImage(slice_real, os.path.join(path, f"{name}_tar_slice_{i}.jpg"))
