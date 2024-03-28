import os.path
# import random
from django.shortcuts import render, redirect
from .models import *
from django.views import View
from .exercise import test_out
from .exercise import Show_result

# Create your views here.


class Index(View):
    def get(self, request):
        img_path = []
        for each_img in Medical.objects.all().values():
            img_path.append(each_img['pre_img'])
            img_path.append(each_img['tar_img'])
            # 交叉插入,待优化
        value = {'img_path': img_path}
        return render(request, 'app1/index.html', context=value)
        # context 以字典赋值，无法遍历 context 本身


class Upload(View):
    def get(self, request):
        return render(request, 'app1/upload.html')

    def post(self, request):
        upload_file = request.FILES.get('upload_file')

        upload_file_name = upload_file.name
        patient_name = upload_file_name[:upload_file_name.find('.')]
        file_folder_path = os.path.join('resource', 'patient', get_time(), patient_name)
        if not os.path.exists(file_folder_path):
            os.makedirs(file_folder_path)
        # 在 /resource 中不重复地创建文件夹 /patient /{{ time }} /{{ patient_name }}

        if os.path.exists(os.path.join(file_folder_path, upload_file_name)):
            return redirect('index')  # 文件已存在，跳过
            # upload_image_name = upload_image_name.replace('.',
            # '_' +
            # ''.join(random.SystemRandom().choice(
            # string.ascii_letters + string.digits)
            # for _ in range(8))
            # + '.')

        patient = Medical.objects.create(name=patient_name, raw_file=upload_file)
        test_out.generate_mha(file_folder_path)
        Show_result.generate_img(folder_path=file_folder_path, patient_name=patient_name)
        # 文件处理及重命名

        patient.pre_img.name = os.path.join('patient', get_time(), patient_name, patient_name + '_pre.png')
        patient.tar_img.name = os.path.join('patient', get_time(), patient_name, patient_name + '_tar.png')
        patient.save()
        return redirect('index')


class Search(View):
    def get(self, request):
        if not request.GET:
            return render(request, 'app1/search.html')
        tags = request.GET['tags']
        # print(tags)
        img_path = []
        for each_img in Medical.objects.filter(name=tags).values():
            img_path.append(each_img['pre_img'])
            img_path.append(each_img['tar_img'])
            # 交叉插入,待优化
        value = {'img_path': img_path}
        # 模糊搜索待添加
        return render(request, 'app1/search.html', context=value)
