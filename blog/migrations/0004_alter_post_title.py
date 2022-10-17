# Generated by Django 4.1 on 2022-10-17 05:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0003_alter_post_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="title",
            field=models.CharField(
                max_length=250,
                validators=[django.core.validators.MinLengthValidator(20)],
            ),
        ),
    ]
