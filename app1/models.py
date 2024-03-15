from django.db import models
from django.utils import timezone
from .get_time import get_time
from .validator import validate_file_extension
import os
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
# Create your models here.


class Photo(models.Model):
    title = models.CharField(max_length=1000)
    date = models.DateField(auto_now_add=True)

    raw_image = models.ImageField(default='null',
                                upload_to=os.path.join('img', get_time()),
                                validators=[validate_file_extension])

    new_image = models.ImageField(default='null',
                                upload_to=os.path.join('img', get_time()),
                                validators=[validate_file_extension])

    def __str__(self):
        return f'{self.title}'
