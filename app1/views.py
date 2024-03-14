import requests
import time
import os
from django.shortcuts import render, redirect
from .models import *
from . import trans
from .form import UploadImage
from django.views import View
from django.conf import settings
from django.core.files.storage import FileSystemStorage as Fss
# Create your views here.


class Index(View):
    def get(self, request):
        value = {'contents': Goods.objects.all(), 'test': Goods.objects.all(), 'img': Photo.objects.all()}
        return render(request, 'app1/index.html', context=value)
        # context 以字典赋值，无法遍历 context 本身


class Upload(View):
    def get(self, request):
        return render(request, 'app1/upload.html')

    def post(self, request):
        local_time = time.localtime(time.time())
        time_pin = (str(local_time.tm_year).zfill(4) +
                    str(local_time.tm_mon).zfill(2) +
                    str(local_time.tm_mday).zfill(2))
        img_path = os.path.join('resource', 'img', time_pin)
        if not os.path.exists(img_path):
            os.mkdir(img_path)

        my_file = request.FILES.get('my_file')
        trans.transform(my_file, my_file.name)
        files = {'image': open('/home/byte/PycharmProjects/website/chart/resource/img/' + my_file.name, 'rb')}
        requests.post(url='http://127.0.0.1/app1/upload', files=files)
        file2 = request.FILES.get('image')
        Photo.objects.create(title=my_file.name, my_file=file2) # moxing shi jian bug
        return redirect('index')

