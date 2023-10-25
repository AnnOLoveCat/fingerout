# Generated by Django 3.2.18 on 2023-10-23 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
        migrations.CreateModel(
            name='Mails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mail', models.CharField(max_length=50)),
                ('used', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('url', models.URLField()),
                ('mail', models.CharField(max_length=50)),
                ('line_id', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Ministry_Interior',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line_id', models.CharField(max_length=50)),
                ('inform_date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news_title', models.CharField(max_length=50)),
                ('post_time', models.DateTimeField(auto_now=True)),
                ('news_content', models.CharField(max_length=1000)),
            ],
        ),
    ]
