# Generated by Django 4.2.7 on 2024-07-08 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('b2', '0018_certificaterecord_uploaded_certificate'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificaterecord',
            name='certificate_name',
            field=models.CharField(default='', max_length=100),
        ),
    ]