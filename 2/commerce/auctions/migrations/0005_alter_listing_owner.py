# Generated by Django 3.2.5 on 2021-08-02 18:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_listing_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='listings', to='auctions.user'),
            preserve_default=False,
        ),
    ]
