# Generated by Django 3.2.5 on 2021-08-02 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TodoForm',
            new_name='Todo',
        ),
    ]