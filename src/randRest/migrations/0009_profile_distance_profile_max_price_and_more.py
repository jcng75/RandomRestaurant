# Generated by Django 4.1.4 on 2023-05-06 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('randRest', '0008_remove_profile_restaurants'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='distance',
            field=models.IntegerField(default=500),
        ),
        migrations.AddField(
            model_name='profile',
            name='max_price',
            field=models.IntegerField(default=2),
        ),
        migrations.AddField(
            model_name='profile',
            name='restaurants',
            field=models.ManyToManyField(blank=True, to='randRest.restaurant'),
        ),
    ]
