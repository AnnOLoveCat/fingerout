# Generated by Django 3.2.18 on 2023-09-28 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fingerlinebot', '0003_auto_20230607_0612'),
    ]

    operations = [
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=50)),
                ('web_link', models.CharField(max_length=500)),
                ('domain_name', models.CharField(max_length=50)),
                ('build_time', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
