from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

class CertificateRecord(models.Model):
    certificate_number = models.CharField(max_length=100)
    printed = models.BooleanField(default=False)
    dispatched = models.BooleanField(default=False)
    picked_by = models.CharField(max_length=100, blank=True, default='')  
    printed_by = models.ForeignKey(User, related_name='printed_certificates', on_delete=models.SET_NULL, null=True, blank=True)
    print_date = models.DateTimeField(auto_now_add=True)
    dispatched_to = models.CharField(max_length=100, blank=True)
    dispatched_by = models.ForeignKey(User, related_name='dispatched_certificates', on_delete=models.SET_NULL, null=True, blank=True)
    dispatch_date = models.DateTimeField(null=True, blank=True)
    uploaded_file_path = models.CharField(max_length=255, blank=True)  
    uploaded_certificate = models.FileField(upload_to='certificates/%Y/%m/%d/', blank=True, null=True)
    def is_pdf(self):
        return self.uploaded_certificate and self.uploaded_certificate.name.lower().endswith('.pdf')
    
    def is_image(self):
        return self.uploaded_certificate and self.uploaded_certificate.name.lower().endswith(('.jpg', '.jpeg', '.png'))
    uploaded_certificate = models.FileField(upload_to='certificates/%Y/%m/%d/', blank=True, default='path/to/default_certificate.pdf')  

class DispatchRecord(models.Model):
    certificate = models.OneToOneField(CertificateRecord, on_delete=models.CASCADE)
    dispatched_by = models.ForeignKey(User, on_delete=models.CASCADE)
    dispatch_phone = models.CharField(max_length=15, blank=True)
    dispatch_date = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.certificate.certificate_number 
