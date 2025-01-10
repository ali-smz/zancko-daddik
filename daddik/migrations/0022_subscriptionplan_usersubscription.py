# Generated by Django 5.1.4 on 2025-01-04 11:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daddik', '0021_message_read'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('free', 'Free'), ('bronze', 'Bronze'), ('silver', 'Silver'), ('gold', 'Gold')], max_length=20, unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('duration', models.DurationField()),
                ('features', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField()),
                ('plan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='daddik.subscriptionplan')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='subscription', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]