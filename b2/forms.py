from django import forms
from .models import CertificateRecord, DispatchRecord, Certificates
from django.contrib.auth.models import User
from django.db import models

class CertificatesForm(forms.ModelForm):
    class Meta:
        model = Certificates
        fields = ['certificate_number', 'certificate_file']
class DispatchForm(forms.ModelForm):
    picked_by_email = forms.EmailField(required=False)
    picked_by_phone = forms.CharField(max_length=15, required=False, label='Phone Number')
    picked_by_wells_fargo = forms.BooleanField(required=False, label='Wells Fargo')

    class Meta:
        model = CertificateRecord
        fields = ['picked_by_email', 'picked_by_phone', 'picked_by_wells_fargo']
