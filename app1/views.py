import os.path

from django.http import HttpResponse
from django.shortcuts import render, redirect

from .b64_to_img import b64_to_img
from .models import *
from django.views import View
import base64, requests, json

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
        upload_time = get_time()
        folder_path = os.path.join('resource', 'patient', upload_time, patient_name)
        if os.path.exists(os.path.join(folder_path, patient_name)):
            value = {'msg': '上传文件重复'}
            return render(request, 'app1/predict.html', context=value)  # 文件已存在，跳过

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        # 在 /resource 中不重复地创建文件夹 /patient /{{ time }} /{{ patient_name }}

        # upload_image_name = upload_image_name.replace('.',
        # '_' +
        # ''.join(random.SystemRandom().choice(
        # string.ascii_letters + string.digits)
        # for _ in range(8))
        # + '.')
        # 重复文件添加随机后缀

        patient = Medical.objects.create(name=patient_name, raw_file=upload_file)

        # test_out.generate_mha(file_folder_path)
        # Show_result.generate_img(folder_path=file_folder_path, patient_name=patient_name)
        # 文件处理及重命名

        raw_file = upload_file.read()
        encoded_data = base64.b64encode(raw_file).decode('utf-8')
        data_dict = {
            'raw_file': encoded_data,
            'time': upload_time,
            'patient_name': patient_name,
        }
        data_json = json.dumps(data_dict)
        url = 'http://10.106.13.36:12500/predict'
        response = requests.post(url, json=data_json, headers={'Content-Type': 'application/json'})

        if response.status_code == 200:
            print('OK!')
            data_return = response.json()
            pre_img_data = base64.b64decode(data_return['pre_img'])
            tar_img_data = base64.b64decode(data_return['tar_img'])
            b64_to_img(os.path.join(folder_path, patient_name + '_pre.png'), pre_img_data)
            b64_to_img(os.path.join(folder_path, patient_name + '_tar.png'), tar_img_data)
            patient.pre_img.name = os.path.join(folder_path, patient_name + '_pre.png')
            patient.tar_img.name = os.path.join(folder_path, patient_name + '_tar.png')
            patient.save()
            value = {'patient': patient}
            return render(request, 'app1/predict.html', context=value)
        elif response.status_code == 408:
            print(408)
            return HttpResponse(status=503)
        else:
            return HttpResponse(status=500)


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
        return render(request, 'app1/detail.html', context=value)
    # 重复性，url待修改
    # 搜索多个待修改
