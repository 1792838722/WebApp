import requests
import time
import os

from PIL import Image
from django.shortcuts import render, redirect
from .models import *
from django.views import View
# Create your views here.


class Index(View):
    def get(self, request):
        value = {'img': Photo.objects.all()} # 修复模板问题
        return render(request, 'app1/index.html', context=value)
        # context 以字典赋值，无法遍历 context 本身


class Upload(View):
    def get(self, request):
        return render(request, 'app1/upload.html')

    def post(self, request):
        img_path = os.path.join('resource', 'img', get_time())
        if not os.path.exists(img_path):
            os.mkdir(img_path)

        my_file = request.FILES.get('my_file')
        if my_file:
            with open(os.path.join(img_path, my_file.name), 'wb+') as write_destination:
                for chunks in my_file.chunks():
                    write_destination.write(chunks)
        raw_img = Image.open(os.path.join(img_path, my_file.name))
        new_img = raw_img.rotate(90)
        new_img_name = my_file.name.replace('.', 'new.')
        new_img.save(os.path.join(img_path, new_img_name))
        photo = Photo.objects.create(title=new_img_name)
        photo.my_file.name = os.path.join('img', get_time(), new_img_name)
        photo.save()
        return redirect('index')

