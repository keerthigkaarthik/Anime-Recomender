# Generated by Django 4.0 on 2021-12-26 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weeb_shit', '0002_list_of_anime_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='list_of_anime',
            name='type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
