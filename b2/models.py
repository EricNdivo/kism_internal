from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class CertificateRecord(models.Model):
    certificate_number = models.CharField(max_length=50, unique=True)
    printed = models.BooleanField(default=False)
    dispatched = models.BooleanField(default=False)
    picked_by = models.ForeignKey(User, related_name='picked_certificates', on_delete=models.SET_NULL, null=True, blank=True)
    printed_by = models.ForeignKey(User, related_name='printed_certificates', on_delete=models.SET_NULL, null=True, blank=True)
    dispatched_to = models.EmailField(null=True, blank=True)
    dispatch_phone = models.CharField(max_length=20, null=True, blank=True)
    print_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.certificate_number

class DispatchRecord(models.Model):
    certificate_number = models.CharField(max_length=50, default=True)
    dispatched_by = models.ForeignKey(User, on_delete=models.CASCADE)
    dispatch_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Certificate {self.certificate_number} dispatched by {self.dispatched_by.username}"

class DailyRecord(models.Model):
    date = models.DateField(auto_now_add=True)
    printed_certificates = models.CharField(max_length=255)  
    dispatched_certificates = models.ManyToManyField(CertificateRecord, related_name='dispatched_daily_records')


    def __str__(self):
        return f"Records for {self.date}"
