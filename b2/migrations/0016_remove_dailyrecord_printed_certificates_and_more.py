# Generated by Django 4.2.7 on 2024-07-03 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('b2', '0015_remove_dispatchrecord_dispatched_phone_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dailyrecord',
            name='printed_certificates',
        ),
        migrations.AddField(
            model_name='dailyrecord',
            name='printed_certificates',
            field=models.ManyToManyField(related_name='printed_daily_records', to='b2.certificaterecord'),
        ),
    ]
