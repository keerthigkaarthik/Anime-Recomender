# Generated by Django 4.0 on 2022-02-24 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weeb_shit', '0010_remove_profile_anime_1_remove_profile_anime_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='fav',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
