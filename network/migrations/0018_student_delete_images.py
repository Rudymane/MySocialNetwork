# Generated by Django 4.1.1 on 2022-11-18 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0017_remove_images_user_images_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('avatar', models.ImageField(upload_to='uploads/')),
            ],
        ),
        migrations.DeleteModel(
            name='Images',
        ),
    ]
