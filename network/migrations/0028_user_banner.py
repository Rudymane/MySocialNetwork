# Generated by Django 4.1.1 on 2022-12-06 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0027_alter_posts_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='banner',
            field=models.ImageField(blank=True, default='network/files/userimages/krgq9kqlgbk71.png', upload_to=''),
        ),
    ]
