# Generated by Django 5.0.6 on 2024-07-07 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('b2', '0015_certificates'),
    ]

    operations = [
        migrations.RenameField(
            model_name='certificates',
            old_name='CertificateFile',
            new_name='certificate_file',
        ),
    ]
