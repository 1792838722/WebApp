from django.db import models
from .get_time import get_time
import os


# Create your models here.

def upload_to(instance, filename):
    return os.path.join('patient', get_time(), instance.patient_name, instance.name)


class Medical(models.Model):
    name = models.CharField(max_length=100)
    patient_name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    id = models.AutoField(primary_key=True)

    raw_file = models.FileField(default='null', upload_to=upload_to)

    pre_img = models.ImageField(default='null')

    tar_img = models.ImageField(default='null')

    def __str__(self):
        return f'{self.patient_name}'
