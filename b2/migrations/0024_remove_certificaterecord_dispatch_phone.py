# Generated by Django 4.1.1 on 2024-07-09 15:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('b2', '0023_rename_dispatched_phone_certificaterecord_dispatch_phone_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='certificaterecord',
            name='dispatch_phone',
        ),
    ]
