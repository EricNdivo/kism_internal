# Generated by Django 4.1.1 on 2024-07-09 07:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('b2', '0022_certificaterecord_uploaded_file_path'),
    ]

    operations = [
        migrations.RenameField(
            model_name='certificaterecord',
            old_name='dispatched_phone',
            new_name='dispatch_phone',
        ),
        migrations.RenameField(
            model_name='dispatchrecord',
            old_name='dispatched_phone',
            new_name='dispatch_phone',
        ),
    ]