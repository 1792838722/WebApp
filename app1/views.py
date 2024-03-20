import os.path
import random
import string
from PIL import Image
from django.shortcuts import render, redirect
from .models import *
from django.views import View


# Create your views here.


class Index(View):
    def get(self, request):
        img_path = []
        for each_img in Photo.objects.all().values():
            img_path.append(each_img['raw_image'])
            img_path.append(each_img['new_image'])
            # 交叉插入,待优化
        value = {'img_path': img_path}
        return render(request, 'app1/index.html', context=value)
        # context 以字典赋值，无法遍历 context 本身


class Upload(View):
    def get(self, request):
        return render(request, 'app1/upload.html')

    def post(self, request):
        img_folder = os.path.join('resource', 'img', get_time())
        if not os.path.exists(img_folder):
            os.mkdir(img_folder)
        # 在 /resource 中不重复地创建文件夹

        upload_image = request.FILES.get('upload_file')
        upload_image_name = upload_image.name
        if os.path.exists(os.path.join(img_folder, upload_image_name)):
            upload_image_name = upload_image_name.replace('.',
                                                          '_' +
                                                          ''.join(random.SystemRandom().choice(
                                                              string.ascii_letters + string.digits)
                                                              for _ in range(8))
                                                          + '.')

        if upload_image:
            with open(os.path.join(img_folder, upload_image_name), 'wb+') as write_destination:
                for chunks in upload_image.chunks():
                    write_destination.write(chunks)
        # 保存图片

        raw_img = Image.open(os.path.join(img_folder, upload_image_name))
        new_img = raw_img.rotate(90)
        new_img_name = upload_image_name.replace('.', '_new.')
        new_img.save(os.path.join(img_folder, new_img_name))
        # 文件处理及重命名

        photo = Photo.objects.create(title=upload_image_name[:upload_image_name.find('.')],
                                     extension=upload_image_name[upload_image_name.find('.'):])
        photo.raw_image.name = os.path.join('img', get_time(), upload_image_name)
        photo.new_image.name = os.path.join('img', get_time(), new_img_name)
        photo.save()
        return redirect('index')


class Search(View):
    def get(self, request):
        if not request.GET:
            return render(request, 'app1/search.html')
        tags = request.GET['tags']
        print(tags)
        img_path = []
        for each_img in Photo.objects.filter(title=tags).values():
            img_path.append(each_img['raw_image'])
            img_path.append(each_img['new_image'])
            # 交叉插入,待优化
        value = {'img_path': img_path}
        # 模糊搜索待添加
        return render(request, 'app1/search.html', context=value)
