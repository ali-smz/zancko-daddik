# Generated by Django 5.1.4 on 2025-01-04 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daddik', '0022_subscriptionplan_usersubscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptionplan',
            name='name',
            field=models.CharField(choices=[('free', 'Free'), ('bronze', 'Bronze'), ('silver', 'Silver'), ('gold', 'Gold')], default='free', max_length=20, unique=True),
        ),
    ]
