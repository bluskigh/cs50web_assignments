# Generated by Django 3.2.5 on 2021-08-06 12:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0012_alter_post_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 6, 12, 40, 43, 518930)),
        ),
    ]
