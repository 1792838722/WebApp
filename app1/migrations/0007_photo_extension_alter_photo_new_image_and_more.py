# Generated by Django 4.2.11 on 2024-03-20 06:54

import app1.validator
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0006_remove_photo_my_file_photo_new_image_photo_raw_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='extension',
            field=models.CharField(default='.jpg', max_length=7),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='photo',
            name='new_image',
            field=models.ImageField(default='null', upload_to='img/20240320', validators=[app1.validator.validate_file_extension]),
        ),
        migrations.AlterField(
            model_name='photo',
            name='raw_image',
            field=models.ImageField(default='null', upload_to='img/20240320', validators=[app1.validator.validate_file_extension]),
        ),
    ]