# Generated by Django 3.2.13 on 2024-05-05 23:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cash_collection', '0002_auto_20240505_2338'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='payment_date',
            field=models.DateTimeField(default=False),
        ),
    ]