# Generated by Django 5.1.4 on 2024-12-31 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daddik', '0010_user_delete_legalperson_delete_realperson'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='companyNationalId',
            field=models.CharField(blank=True, max_length=11, null=True, unique=True),
        ),
    ]