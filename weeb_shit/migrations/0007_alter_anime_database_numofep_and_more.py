# Generated by Django 4.0 on 2022-01-23 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('weeb_shit', '0006_anime_database_remove_list_of_anime_genre_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anime_database',
            name='numofep',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='anime_database',
            name='releaseyear',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='anime_database',
            name='score',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.CreateModel(
            name='weebs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profilepic', models.CharField(blank=True, max_length=1000, null=True)),
                ('profilepagepic', models.CharField(blank=True, max_length=1000, null=True)),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('animes_watched', models.CharField(blank=True, max_length=1000000000, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(blank=True, max_length=50, null=True)),
                ('location', models.CharField(blank=True, max_length=30, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('anime_1', models.CharField(blank=True, max_length=1000, null=True)),
                ('anime_id', models.CharField(blank=True, max_length=1000, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
    ]
