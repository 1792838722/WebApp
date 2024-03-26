from PIL import Image
import numpy as np
import itk


# 加载MHA文件
mha_file_path = "F:\\mha\\Unet\\chengang_pre.mha"
image = itk.imread(mha_file_path)
array_view = itk.array_view_from_image(image)

# 将MHA图像转换为PIL图像
image_array = np.squeeze(np.asarray(array_view))
pil_image = Image.fromarray(image_array)

# 保存为JPEG文件
output_jpeg_path = "F:\\jpg\\unet\\chengang_pre.jpg"
pil_image.save(output_jpeg_path)
