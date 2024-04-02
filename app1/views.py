import os.path
from django.shortcuts import render, redirect
from .models import *
from django.views import View
from .exercise import test_out
from .exercise import Show_result


# Create your views here.


class Index(View):
    def get(self, request):
        return render(request, 'app1/index.html')


class Predict(View):
    def get(self, request):
        return render(request, 'app1/predict.html')

    def post(self, request):
        upload_file = request.FILES.get('upload_file')

        upload_file_name = upload_file.name
        patient_name = upload_file_name[:upload_file_name.find('.')]
        file_folder_path = os.path.join('resource', 'patient', get_time(), patient_name)
        if os.path.exists(os.path.join(file_folder_path, patient_name)):
            value = {'msg': '上传文件重复'}
            return render(request, 'app1/predict.html', context=value)  # 文件已存在，跳过

        if not os.path.exists(file_folder_path):
            os.makedirs(file_folder_path)
        # 在 /resource 中不重复地创建文件夹 /patient /{{ time }} /{{ patient_name }}

        # upload_image_name = upload_image_name.replace('.',
        # '_' +
        # ''.join(random.SystemRandom().choice(
        # string.ascii_letters + string.digits)
        # for _ in range(8))
        # + '.')
        # 重复文件添加随机后缀

        patient = Medical.objects.create(name=patient_name, raw_file=upload_file)
        test_out.generate_mha(file_folder_path)
        Show_result.generate_img(folder_path=file_folder_path, patient_name=patient_name)
        # 文件处理及重命名

        patient.pre_img.name = os.path.join('patient', get_time(), patient_name, patient_name + '_pre.png')
        patient.tar_img.name = os.path.join('patient', get_time(), patient_name, patient_name + '_tar.png')
        patient.save()
        value = {'patient': patient}
        return render(request, 'app1/predict.html', context=value)


class Intro(View):
    def get(self, request):
        return render(request, 'app1/intro.html')


class Search(View):
    def get(self, request):
        if not request.GET:
            return render(request, 'app1/search.html')
        tags = request.GET['tags']
        value = {'patients': Medical.objects.filter(name=tags)}
        # 模糊搜索待添加
        return render(request, 'app1/search.html', context=value)


class History(View):
    def get(self, request):
        value = {'patients': Medical.objects.all()}
        return render(request, 'app1/history.html', context=value)


class Detail(View):
    def get(self, request):
        patient_id = request.path_info[(request.path_info.rfind('_') + 1):]
        value = {'patient': Medical.objects.filter(id=patient_id)}
        print(Medical.objects.filter(id=patient_id))
        return render(request, 'app1/detail.html', context=value)
    # 重复性，url待修改
    # 搜索多个待修改
