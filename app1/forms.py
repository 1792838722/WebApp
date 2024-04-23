from django import forms
from django.core.validators import FileExtensionValidator
from .models import *
from datetime import date


class UploadForm(forms.ModelForm):
    class Meta:
        model = Medical
        fields = ['raw_file']
        error_message = {
            'raw_file': {'required': '必须上传文件！'}
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 限制文件上传类型为 npz
        self.fields['raw_file'].validators.append(FileExtensionValidator(['npz']))

    def clean(self):
        cleaned_data = super().clean()
        raw_file = cleaned_data.get('raw_file')
        if raw_file:
            # 检查数据库中是否已经存在相同文件名的记录
            if Medical.objects.filter(name=raw_file.name, date=date.today()).exists():
                raise forms.ValidationError("文件已存在，请选择其他文件。")
        return cleaned_data

    def save(self, commit=True):
        instance = super(UploadForm, self).save(commit=False)
        file_name = self.cleaned_data['raw_file'].name
        instance.name = file_name
        instance.patient_name = file_name[:file_name.rfind('.')]
        if commit:
            instance.save()
        return instance


class SearchForm(forms.Form):
    patient_name = forms.CharField(
        max_length=100,
        required=True,
        label='name',
        error_messages={
            'required': 'required!',
            'max_length': 'max_length!',
        }
    )