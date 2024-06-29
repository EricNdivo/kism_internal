# Generated by Django 4.1.1 on 2024-06-29 07:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('b2', '0003_certificate_printed_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='CertificateRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certificate_number', models.CharField(max_length=50, unique=True)),
                ('printed', models.BooleanField(default=False)),
                ('dispatched', models.BooleanField(default=False)),
                ('dispatched_to', models.EmailField(blank=True, max_length=254, null=True)),
                ('dispatch_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('picked_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='dispatchrecord',
            name='certificate',
        ),
        migrations.AddField(
            model_name='dispatchrecord',
            name='certificate_number',
            field=models.CharField(default=None, max_length=50, null=True),
        ),
        migrations.RemoveField(
            model_name='dailyrecord',
            name='dispatched_certificates',
        ),
        migrations.RemoveField(
            model_name='dailyrecord',
            name='printed_certificates',
        ),
        migrations.DeleteModel(
            name='Certificate',
        ),
        migrations.AddField(
            model_name='dailyrecord',
            name='dispatched_certificates',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='dailyrecord',
            name='printed_certificates',
            field=models.CharField(default='', max_length=255),
        ),
    ]