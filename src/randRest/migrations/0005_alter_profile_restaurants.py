# Generated by Django 4.1.4 on 2023-04-24 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('randRest', '0004_alter_profile_restaurants'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='restaurants',
            field=models.ManyToManyField(blank=True, to='randRest.restaurant'),
        ),
    ]