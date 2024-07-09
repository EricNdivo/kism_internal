from django.contrib import admin
from .models import CertificateRecord, DispatchRecord

admin.site.register(CertificateRecord)
admin.site.register(DispatchRecord)