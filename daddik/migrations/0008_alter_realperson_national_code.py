# Generated by Django 5.1.4 on 2024-12-31 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daddik', '0007_alter_realperson_national_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='realperson',
            name='national_code',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
    ]
