import django_filters
from django_filters import *
from .models import CertificateRecord, DailyRecord, DispatchRecord

class DailyRecordFilter(django_filters.FilterSet):
    printed_certificates = BooleanFilter(field_name='printed_certificates__printed', lookup_expr='icontains', label='Printed Certificates')
    dispatched_certificates = CharFilter(field_name='dispatched_certificates__certificate_number', lookup_expr='icontains', label='Dispatched Certificates')
    class Meta:
        model = DailyRecord
        fields = '__all__'
        exclude = ['date']