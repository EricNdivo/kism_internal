from django import forms
from .models import CertificateRecord, DispatchRecord
from django.contrib.auth.models import User
from django.db import models

class CertificateRecordForm(forms.ModelForm):
    picked_by = forms.ModelChoiceField(queryset=User.objects.all(), empty_label=None, label='Employee Name')
    dispatched_to = forms.EmailField(label='Dispatched To (Email)', required=False)
    dispatch_phone = forms.CharField(max_length=20, label='Dispatch Phone Number', required=False)

    class Meta:
        model = CertificateRecord
        fields = ['certificate_number', 'printed', 'dispatched', 'picked_by', 'dispatched_to', 'dispatch_phone']
        widgets = {
            'printed': forms.Select(choices=((True, 'Yes'), (False, 'No')), attrs={'class': 'form-control'}),
            'dispatched': forms.Select(choices=((True, 'Yes'), (False, 'No')), attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        dispatched = cleaned_data.get('dispatched')
        dispatched_to = cleaned_data.get('dispatched_to')
        dispatch_phone = cleaned_data.get('dispatch_phone')

        if dispatched and (not dispatched_to or not dispatch_phone):
            raise forms.ValidationError('You must provide a dispatched to email and phone number if the certificate is dispatched.')
        
class DispatchForm(forms.ModelForm):
    picked_by_email = forms.EmailField(required=False)
    picked_by_phone = forms.CharField(max_length=15, required=False, label='Phone Number')
    picked_by_wells_fargo = forms.BooleanField(required=False, label='Wells Fargo')

    class Meta:
        model = CertificateRecord
        fields = ['picked_by_email', 'picked_by_phone', 'picked_by_wells_fargo']
