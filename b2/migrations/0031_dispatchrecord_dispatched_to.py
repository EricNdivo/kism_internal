# Generated by Django 4.2.7 on 2024-07-16 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('b2', '0030_alter_dailyrecord_dispatched_certificates_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dispatchrecord',
            name='dispatched_to',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
