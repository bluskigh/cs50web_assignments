# Generated by Django 3.2.5 on 2021-08-06 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0010_auto_20210806_0051'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='updated',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
