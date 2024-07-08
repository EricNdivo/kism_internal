from django.contrib import admin
from .models import CertificateRecord, DailyRecord, DispatchRecord,Certificates

admin.site.register(CertificateRecord)
admin.site.register(DailyRecord)
admin.site.register(DispatchRecord)
admin.site.register(Certificates)