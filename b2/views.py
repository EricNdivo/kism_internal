from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from .models import CertificateRecord, DailyRecord, DispatchRecord
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import CertificatesForm, DispatchForm
from django.contrib.auth.models import User
from django.contrib import messages
from django import forms
@login_required
def certificate_list(request):
    certificates = CertificateRecord.objects.all()
    return render(request, 'certificates/certificate_list.html', {'certificates': certificates})

@login_required
def daily_records(request):
    records = DailyRecord.objects.all()
    return render(request, 'certificates/daily_records.html', {'records': records})

@login_required
def add_certificate(request):
    if request.method == 'POST':
        form = CertificatesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('certificate_list')
    else:
        form = CertificatesForm()
    return render(request, 'certificates/add_certificate.html',{'form':form})

@login_required
def dispatch_certificate(request, certificate_id):
    certificate = get_object_or_404(CertificateRecord, id=certificate_id)
    
    if request.method == 'POST':
        form = DispatchForm(request.POST)
        if form.is_valid():
            picked_by_email = form.cleaned_data.get('picked_by_email')
            picked_by_phone = form.cleaned_data.get('picked_by_phone')
            picked_by_wells_fargo = form.cleaned_data.get('picked_by_wells_fargo')
            
            if picked_by_email:
                certificate.picked_by = picked_by_email
                certificate.dispatched_to = picked_by_email
            elif picked_by_phone:
                certificate.picked_by = picked_by_phone
                certificate.dispatched_phone = picked_by_phone
            elif picked_by_wells_fargo:
                certificate.picked_by = "Wells Fargo"
                certificate.dispatched_to = "Wells Fargo"
            else:
                messages.error(request, "Please provide either an email address, phone number, or select Wells Fargo.")
                return render(request, 'certificates/dispatch_certificate.html', {'certificate': certificate, 'form': form})
            
            certificate.dispatched = True
            certificate.dispatched_by = request.user
            certificate.dispatch_date = timezone.now()
            certificate.save()
            
            dispatch_record = DispatchRecord(
                certificate=certificate,
                dispatched_by=request.user,
                dispatch_date=timezone.now()
            )
            dispatch_record.save()
            
            daily_record, created = DailyRecord.objects.get_or_create(date=timezone.now().date())
            daily_record.dispatched_certificates.add(certificate)
            
            return redirect('certificate_list')
    else:
        form = DispatchForm()
    
    return render(request, 'certificates/dispatch_certificate.html', {'certificate': certificate, 'form': form})

@login_required
def dispatched_certificates(request):
    dispatch_records = DispatchRecord.objects.all()
    return render(request, 'certificates/dispatched_certificates.html', {'dispatch_records': dispatch_records})
