# Generated by Django 4.0 on 2022-02-17 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weeb_shit', '0009_alter_fivestars_user_alter_fourstars_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='anime_1',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='anime_id',
        ),
        migrations.AlterField(
            model_name='fivestars',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='weeb_shit.profile'),
        ),
        migrations.AlterField(
            model_name='fourstars',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='weeb_shit.profile'),
        ),
        migrations.AlterField(
            model_name='onestars',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='weeb_shit.profile'),
        ),
        migrations.AlterField(
            model_name='threestars',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='weeb_shit.profile'),
        ),
        migrations.AlterField(
            model_name='twostars',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='weeb_shit.profile'),
        ),
    ]
