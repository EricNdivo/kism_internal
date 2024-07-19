from django import forms
from .models import CertificateRecord, DispatchRecord
from django.contrib.auth.models import User
from django.db import models

class CertificateRecordForm(forms.ModelForm):
    class Meta:
        model = CertificateRecord
        fields = ['certificate_number', 'uploaded_certificate', 'printed']
        widgets = {
            'printed': forms.Select(choices=[(True, 'Yes'), (False, 'No')])
        }
        
class DispatchForm(forms.ModelForm):
    class Meta:
        model = DispatchRecord
        fields =['dispatched_to', 'dispatched_phone','picked_by_wells_fargo']