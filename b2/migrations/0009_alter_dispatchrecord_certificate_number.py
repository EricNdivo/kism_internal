# Generated by Django 4.1.1 on 2024-06-30 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('b2', '0008_certificaterecord_print_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dispatchrecord',
            name='certificate_number',
            field=models.CharField(default=True, max_length=50),
        ),
    ]
