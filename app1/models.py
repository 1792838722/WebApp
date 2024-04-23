from django.db import models
from django.urls import reverse
import os


# Create your models here.

def upload_to(instance, filename):
    return os.path.join('patient',
                        ''.join([instance.date.year, instance.date.month, instance.date.day]),
                        instance.patient_name, instance.name)


class Medical(models.Model):
    name = models.CharField(max_length=100, blank=False)
    patient_name = models.CharField(max_length=100, blank=False)
    date = models.DateField(auto_now_add=True)
    id = models.AutoField(primary_key=True)

    raw_file = models.FileField(upload_to=upload_to, blank=False)

    pre_img = models.ImageField(blank=False)

    tar_img = models.ImageField(blank=False)

    def __str__(self):
        return f'{self.patient_name}'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.pk})
