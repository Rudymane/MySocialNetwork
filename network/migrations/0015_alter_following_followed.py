# Generated by Django 4.1.1 on 2022-11-14 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0014_alter_following_followed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='following',
            name='followed',
            field=models.CharField(max_length=40),
        ),
    ]
