# Generated by Django 4.2.7 on 2024-07-05 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('b2', '0017_certificaterecord_uploaded_file_path_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificaterecord',
            name='uploaded_certificate',
            field=models.FileField(blank=True, null=True, upload_to='certificates/%Y/%m/%d/'),
        ),
    ]
