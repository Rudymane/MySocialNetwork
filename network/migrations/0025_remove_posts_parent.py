# Generated by Django 4.1.1 on 2022-12-01 16:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0024_posts_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posts',
            name='parent',
        ),
    ]
