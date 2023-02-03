# Generated by Django 4.1.1 on 2022-11-18 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0018_student_delete_images'),
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='network/files/userimages')),
            ],
        ),
        migrations.DeleteModel(
            name='Student',
        ),
    ]