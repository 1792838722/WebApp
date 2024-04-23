import os.path
from django.shortcuts import render
from .models import *
from django.views import View
from django.views.generic import ListView, FormView, DetailView
from .exercise import test_out, Show_result
from .forms import UploadForm, SearchForm


# Create your views here.


class Index(View):
    def get(self, request):
        return render(request, 'app1/index.html')


class Predict(View):
    def get(self, request):
        form = UploadForm()
        return render(request, 'app1/predict.html', context={'form': form})

    def post(self, request):
        form = UploadForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            instance = form.save()
            relate_path = os.path.join('patient',
                                       ''.join([instance.date.year, instance.date.month, instance.date.day]),
                                       instance.patient_name, instance.patient_name)
            folder_path = os.path.join('resource', relate_path)
            test_out.generate_mha(folder_path)
            Show_result.generate_img(folder_path=folder_path, patient_name=instance.patient_name)
            instance.pre_img.name = ''.join([relate_path, '_pre.png'])
            instance.tar_img.name = ''.join([relate_path, '_tar.png'])
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


class Search(ListView, FormView):
    model = Medical
    template_name = 'app1/search.html'
    context_object_name = 'patients'
    paginate_by = 5
    form_class = SearchForm

    def get_queryset(self):
        queryset = super().get_queryset()
        form = self.form_class(self.request.GET)
        if form.is_valid():
            return queryset.filter(patient_name=form.cleaned_data['patient_name'])
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['form'] = self.get_form()
        return context


class History(ListView, FormView):
    model = Medical
    template_name = 'app1/history.html'
    context_object_name = 'patients'
    paginate_by = 5
    form_class = SearchForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context


class Detail(DetailView):
    model = Medical
    template_name = 'app1/detail.html'
    context_object_name = 'patient'
    # 搜索多个待修改
