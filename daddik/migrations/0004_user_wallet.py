# Generated by Django 5.1.4 on 2025-02-16 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daddik', '0003_user_education'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='wallet',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=15),
        ),
    ]
