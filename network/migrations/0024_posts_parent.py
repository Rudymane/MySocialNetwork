# Generated by Django 4.1.1 on 2022-12-01 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0023_alter_profiles_user_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='parent',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='network.posts'),
        ),
    ]