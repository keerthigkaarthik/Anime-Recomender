# Generated by Django 4.0 on 2021-12-26 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='list_of_anime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numofep', models.CharField(blank=True, max_length=4, null=True)),
                ('releaseyear', models.CharField(blank=True, max_length=4, null=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('picture', models.CharField(blank=True, max_length=1000, null=True)),
                ('slug', models.SlugField(default='test')),
                ('synopsis', models.CharField(blank=True, max_length=100000, null=True)),
            ],
        ),
    ]
