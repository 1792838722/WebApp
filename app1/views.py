from PIL import Image
from django.shortcuts import render, redirect
from .models import *
from django.views import View
# Create your views here.


class Index(View):
    def get(self, request):
        raw_img_path = []
        new_img_path = []
        for each_img in Photo.objects.all().values():
            raw_img_path.append(each_img['raw_image'])
            new_img_path.append(each_img['new_image'])
        value = {'raw_img_path': raw_img_path, 'new_img_path': new_img_path}
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
        if upload_image:
            with open(os.path.join(img_folder, upload_image.name), 'wb+') as write_destination:
                for chunks in upload_image.chunks():
                    write_destination.write(chunks)
        # 保存图片

        raw_img = Image.open(os.path.join(img_folder, upload_image.name))
        new_img = raw_img.rotate(90)
        new_img_name = upload_image.name.replace('.', 'new.')
        new_img.save(os.path.join(img_folder, new_img_name))
        # 文件处理及重命名

        photo = Photo.objects.create(title=upload_image.name)
        photo.raw_image.name = os.path.join('img', get_time(), upload_image.name)
        photo.new_image.name = os.path.join('img', get_time(), new_img_name)
        photo.save()
        return redirect('index')

