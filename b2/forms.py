from django import forms
from .models import CertificateRecord, DispatchRecord, certificates
from django.contrib.auth.models import User
from django.db import models

class CertificatesForm(forms.ModelForm):
    certificate_number = forms.CharField(max_length=100, label='Certificate number')
    CertificateFile = forms.FileField(required=True, label='Upload Certificate')

    class Meta:
        model = certificates
        fields = ['certificate_number', 'CertificateFile']
class DispatchForm(forms.ModelForm):
    picked_by_email = forms.EmailField(required=False)
    picked_by_phone = forms.CharField(max_length=15, required=False, label='Phone Number')
    picked_by_wells_fargo = forms.BooleanField(required=False, label='Wells Fargo')

    class Meta:
        model = CertificateRecord
        fields = ['picked_by_email', 'picked_by_phone', 'picked_by_wells_fargo']
