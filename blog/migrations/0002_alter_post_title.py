# Generated by Django 4.1 on 2022-10-11 09:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="title",
            field=models.CharField(
                max_length=250,
                validators=[django.core.validators.MinLengthValidator(4)],
            ),
        ),
    ]
