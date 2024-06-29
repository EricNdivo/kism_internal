from django import forms
from .models import CertificateRecord, DispatchRecord
from django.contrib.auth.models import User
from django.db import models

class CertificateRecordForm(forms.ModelForm):
    picked_by = forms.ModelChoiceField(queryset=User.objects.all(), empty_label=None, label='Employee Name')
    dispatched_to = forms.EmailField(label='Dispatched To (Email)', required=False)
    dispatch_phone = forms.CharField(max_length=20, label='Dispatch Phone Number', required=False)

    class Meta:
        model = CertificateRecord  # Update model reference
        fields = ['certificate_number', 'printed', 'dispatched', 'picked_by', 'dispatched_to', 'dispatch_phone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['printed'].widget = forms.Select(choices=((True, 'Yes'), (False, 'No')), attrs={'class': 'form-control'})
        self.fields['dispatched'].widget = forms.Select(choices=((True, 'Yes'), (False, 'No')), attrs={'class': 'form-control'})


class DispatchForm(forms.ModelForm):
    class Meta:
        model = DispatchRecord
        fields = ['certificate_number', 'dispatched_by']
