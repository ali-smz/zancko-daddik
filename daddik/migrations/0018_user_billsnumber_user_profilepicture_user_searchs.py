# Generated by Django 5.1.4 on 2025-01-03 09:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daddik', '0017_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='billsNumber',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(3)]),
        ),
        migrations.AddField(
            model_name='user',
            name='profilePicture',
            field=models.FileField(blank=True, upload_to='uploads/images'),
        ),
        migrations.AddField(
            model_name='user',
            name='searchs',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(7)]),
        ),
    ]