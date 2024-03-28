from django.db import models
from django.utils import timezone
from .get_time import get_time
from .validator import validate_file_extension
import os
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage


# Create your models here.

def upload_to(instance, filename):
    return os.path.join('patient', get_time(), instance.name, instance.name)


class Medical(models.Model):
    name = models.CharField(max_length=1000)
    date = models.DateField(auto_now_add=True)

    raw_file = models.FileField(default='null',
                                upload_to=upload_to)

    pre_img = models.ImageField(default='null')

    tar_img = models.ImageField(default='null')

    def __str__(self):
        return f'{self.name}'
