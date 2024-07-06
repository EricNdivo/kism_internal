# Generated by Django 4.2.7 on 2024-07-05 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('b2', '0016_remove_dailyrecord_printed_certificates_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificaterecord',
            name='uploaded_file_path',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='dispatchrecord',
            name='dispatched_phone',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AlterField(
            model_name='certificaterecord',
            name='dispatched_to',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='certificaterecord',
            name='picked_by',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.RemoveField(
            model_name='dailyrecord',
            name='printed_certificates',
        ),
        migrations.AddField(
            model_name='dailyrecord',
            name='printed_certificates',
            field=models.CharField(default='', max_length=255),
        ),
    ]
