from django.db import models
from django.contrib.auth.models import User

class CertificateRecord(models.Model):
    certificate_number = models.CharField(max_length=100)
    printed = models.BooleanField(default=False)
    dispatched = models.BooleanField(default=False)
    picked_by = models.CharField(max_length=100, blank=True, default='')  # Set default value here
    printed_by = models.ForeignKey(User, related_name='printed_certificates', on_delete=models.SET_NULL, null=True, blank=True)
    print_date = models.DateTimeField(auto_now_add=True)
    dispatched_to = models.CharField(max_length=100, blank=True)
    dispatched_phone = models.CharField(max_length=15, blank=True)
    dispatched_by = models.ForeignKey(User, related_name='dispatched_certificates', on_delete=models.SET_NULL, null=True, blank=True)
    dispatch_date = models.DateTimeField(null=True, blank=True)

class DispatchRecord(models.Model):
    certificate = models.OneToOneField(CertificateRecord, on_delete=models.CASCADE)
    dispatched_by = models.ForeignKey(User, on_delete=models.CASCADE)
    dispatched_phone = models.CharField(max_length=15, blank=True)
    dispatch_date = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.certificate.certificate_number 

class DailyRecord(models.Model):
    date = models.DateField(auto_now_add=True)
    printed_certificates = models.CharField(max_length=255)  
    dispatched_certificates = models.ManyToManyField(CertificateRecord, related_name='dispatched_daily_records')

    def __str__(self):
        return f"Records for {self.date}"
