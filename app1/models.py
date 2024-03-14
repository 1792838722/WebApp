

from django.db import models
from django.utils import timezone

from .validator import validate_file_extension
import os
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
# Create your models here.


class Goods(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField(default=0)

    def __str__(self):
        return f"测试商品价格"  # 这里是为了方便在 admin 内查看类，__str__ 本身相当于 Java 的 toString


class Photo(models.Model):
    title = models.CharField(max_length=1000)
    date = models.DateField(auto_now_add=True)
    my_file = models.ImageField(default='null',
                                upload_to=os.path.join('img', str(date).replace('-','')),
                                validators=[validate_file_extension])

    def __str__(self):
        return f'{self.title}'
