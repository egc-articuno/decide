# Generated by Django 2.0 on 2019-12-04 09:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0011_auto_20191204_0916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partycongresscandidate',
            name='postal_code',
            field=models.CharField(max_length=5, validators=[django.core.validators.RegexValidator('^[0-9]{5}$')]),
        ),
        migrations.AlterField(
            model_name='partypresidentcandidate',
            name='postal_code',
            field=models.CharField(max_length=5, validators=[django.core.validators.RegexValidator('^[0-9]{5}$')]),
        ),
    ]
