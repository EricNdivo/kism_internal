# Generated by Django 4.1.1 on 2024-07-02 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('b2', '0012_alter_certificaterecord_picked_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificaterecord',
            name='picked_by',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]