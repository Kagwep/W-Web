# Generated by Django 3.2.9 on 2022-07-20 22:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0005_auto_20220717_1440'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mystory',
            name='participants',
        ),
    ]
