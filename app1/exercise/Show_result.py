import numpy as np
import SimpleITK as sitk
import matplotlib.pyplot as plt
import itk
from PIL import Image

# 输入为两个二进制图像的numpy数组
def dice_coefficient(seg_pred, seg_gt):
    # 计算分割结果和真实标签的交集
    intersection = np.sum(seg_pred * seg_gt)
    # 计算分割结果和真实标签的像素总数
    total = np.sum(seg_pred) + np.sum(seg_gt)

    # 计算Dice系数
    dice = (2. * intersection) / (total + 1e-8)  # 添加一个小的常数以防分母为0

    return dice


def jaccard_coefficient(seg_pred, seg_gt):
    # 计算分割结果和真实标签的交集
    intersection = np.sum(seg_pred * seg_gt)
    # 计算分割结果和真实标签的并集
    union = np.sum(seg_pred) + np.sum(seg_gt) - intersection

    # 计算Jaccard系数（IoU）
    jaccard = intersection / (union + 1e-8)  # 添加一个小的常数以防分母为0

    return jaccard

def transfrom_format(file_path):
    image = itk.imread(file_path)

    # 获取图像数据
    array_view = itk.array_view_from_image(image)
    image_array = np.squeeze(np.asarray(array_view))

    # 选择中间切片
    slice_index = 80
    slice_image = image_array[slice_index, :, :]
    # 转换为PIL图像并保存为JPEG文件
    pil_image = Image.fromarray(slice_image.astype(np.uint8))
    output_jpeg_path = "D:/data/out/baoyongyuan_pre.jpg"
    pil_image.save(output_jpeg_path)


if __name__ == '__main__':
    # 读取.mha文件
    # image = sitk.ReadImage("/home/user/data/lost+found/mha/caidaiping_tar.mha")
    image_pre = sitk.ReadImage("D:/data/out/baoyongyuan_pre.mha")
    image_tar = sitk.ReadImage("D:/data/out/baoyongyuan_tar.mha")
    # 将SimpleITK图像对象转换为NumPy数组
    image_pre_array = sitk.GetArrayFromImage(image_pre)
    image_tar_array = sitk.GetArrayFromImage(image_tar)
    # 将三维数组展开成二维数组
    num_slices = image_pre_array.shape[0]
    num_slices = image_tar_array.shape[0]
    # 将三维数组重塑为二维数组
    image_pre_array_2d = np.reshape(image_pre_array, (image_pre_array.shape[0], -1))
    image_tar_array_2d = np.reshape(image_tar_array, (image_tar_array.shape[0], -1))
    # 恢复图像形状
    pre_restored_image = np.reshape(image_pre_array_2d, (image_pre_array.shape[0], image_pre_array.shape[1], image_pre_array.shape[2]))
    tar_restored_image = np.reshape(image_tar_array_2d, (image_tar_array.shape[0], image_tar_array.shape[1], image_tar_array.shape[2]))
    pre = pre_restored_image[80]
    tar = tar_restored_image[80]


    dice = dice_coefficient(pre,tar)
    print(f"dice数值：{dice}")
    jaccard = jaccard_coefficient(pre,tar)
    print(f"jaccard数值：{jaccard}")
    # transfrom_format("D:/data/out/baoyongyuan_pre.mha")

    # 创建一个2x1的子图
    # fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    # 在第一个子图中显示并存储预测图像
    plt.imshow(pre, cmap='gray')
    plt.title('Predicted Image')
    plt.axis('off')
    plt.savefig('D:/data/out/baoyongyuan_pre.png')
    plt.close()
    # 在第二个子图中显示并存储目标图像
    plt.imshow(tar, cmap='gray')
    plt.title('Target Image')
    plt.axis('off')
    plt.savefig('D:/data/out/baoyongyuan_tar.png')
    plt.close()

    # 显示图像
    # plt.show()
