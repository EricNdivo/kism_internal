# Generated by Django 5.0.7 on 2024-07-17 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('b2', '0031_dispatchrecord_dispatched_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='dispatchrecord',
            name='picked_by_wells_fargo',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]