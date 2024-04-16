import os.path
from django.shortcuts import render, redirect
from .models import *
from django.views import View
from .exercise import test_out
from .exercise import Show_result
from .forms import UploadForm


# Create your views here.


class Index(View):
    def get(self, request):
        return render(request, 'app1/index.html')


class Predict(View):
    def get(self, request):
        form = UploadForm()
        value = {'form': form}
        return render(request, 'app1/predict.html', context=value)

    def post(self, request):
        form = UploadForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            instance = form.save()
            folder_path = os.path.join('resource', 'patient', get_time(), instance.patient_name)
            test_out.generate_mha(folder_path)
            Show_result.generate_img(folder_path=folder_path, patient_name=instance.patient_name)
            instance.pre_img.name = os.path.join('patient', get_time(),
                                                 instance.patient_name, instance.patient_name + '_pre.png')
            instance.tar_img.name = os.path.join('patient', get_time(),
                                                 instance.patient_name, instance.patient_name + '_tar.png')
            instance.save()
            value = {
                'patient': instance,
                'form': form
                }
        else:
            value = {
                'patient': None,
                'form': form
            }
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
    def get(self, request, str_id):
        patient_name, patient_id = str_id.split('_')
        value = {'patient': Medical.objects.filter(id=patient_id), 'patient_name': patient_name}
        return render(request, 'app1/detail.html', context=value)
    # 重复性，url待修改
    # 搜索多个待修改
