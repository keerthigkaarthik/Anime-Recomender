# Generated by Django 4.0 on 2022-02-25 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weeb_shit', '0011_profile_fav'),
    ]

    operations = [
        migrations.CreateModel(
            name='watchedgenre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=1000, null=True)),
                ('count', models.IntegerField()),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='weeb_shit.profile')),
            ],
        ),
    ]
