# Generated by Django 3.2.5 on 2021-07-20 00:58

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pizza',
            name='toppingsarray',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=64), blank=True, null=True, size=None),
        ),
    ]