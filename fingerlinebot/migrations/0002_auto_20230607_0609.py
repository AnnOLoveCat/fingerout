# Generated by Django 3.2.18 on 2023-06-06 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fingerlinebot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ministry_interior',
            name='inform_date',
            field=models.DateField(auto_created='%Y/%m/%d', blank=True),
        ),
        migrations.AlterField(
            model_name='news',
            name='post_time',
            field=models.DateTimeField(auto_created='%Y/%m/%d %H:%M', blank=True),
        ),
    ]
