# Generated by Django 4.1.1 on 2024-07-09 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('b2', '0024_remove_certificaterecord_dispatch_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificaterecord',
            name='dispatched_phone',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.DeleteModel(
            name='DailyRecord',
        ),
    ]