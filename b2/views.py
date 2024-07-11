from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from .models import CertificateRecord, DispatchRecord, DailyRecord
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import CertificateRecordForm, DispatchForm
from django.contrib.auth.models import User
from django.contrib import messages
from django import forms
from django.conf import settings
import os

@login_required
def certificate_list(request):
    certificates = CertificateRecord.objects.all()
    return render(request, 'certificates/certificate_list.html', {'certificates': certificates})

@login_required
def add_certificate(request):
    if request.method == 'POST':
        form = CertificateRecordForm(request.POST, request.FILES)
        certificate_number = request.POST.get('certificate_number')
        uploaded_certificate = request.FILES.get('uploaded_certificate')

        if CertificateRecord.objects.filter(certificate_number=certificate_number).exists():
            messages.error(request, 'Certificate with this number already Exists')
        elif not uploaded_certificate:
            messages.error(request, 'Please upload a certificate')
        else:
            if form.is_valid():
                certificate = form.save(commit=False)
                certificate.printed_by = request.user
                certificate.printed = True
                certificate.save()

                today = timezone.now().date()
                daily_record, created = DailyRecord.objects.get_or_create(date=today)
                daily_record.printed_certificates.add(certificate)

                messages.success(request, 'Certificate added Successfully.')
                return redirect('certificate_list')
            else:
                messages.error(request, 'Form is not valid.')
    else:
        return render(request, 'certificates/add_certificate.html', {'form': form})
    
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
                dispatch_phone=certificate.dispatched_phone, 
                dispatch_date=timezone.now()
            )
            dispatch_record.save()
            
            today = timezone.now().date()
            daily_record, created = DailyRecord.objects.get_or_create(date=today)
            daily_record.dispatched_certificates.add(certificate)
            
            messages.success(request, 'Certificate dispatched successfully.')
            return redirect('certificate_list')
    else:
        form = DispatchForm()
    
    return render(request, 'certificates/dispatch_certificate.html', {'certificate': certificate, 'form': form})

@login_required
def dispatched_certificates(request):
    dispatch_records = DispatchRecord.objects.all()
    return render(request, 'certificates/dispatched_certificates.html', {'dispatch_records': dispatch_records})

def add_certificate(request):
    if request.method == 'POST':
        form = CertificateRecordForm(request.POST, request.FILES)
        certificate_number = request.POST.get('certificate_number')
        uploaded_certificate = request.FILES.get('uploaded_certificate')

        if CertificateRecord.objects.filter(certificate_number=certificate_number).exists():
            messages.error(request, 'Certificate with this number already exists.')
        elif not uploaded_certificate:
            messages.error(request, 'Please upload a certificate.')
        else:
            if form.is_valid():
                form.save()
                messages.success(request, 'Certificate added successfully.')
                return redirect('certificate_list')
            else:
                messages.error(request, 'Form is not valid.')
    else:
        form = CertificateRecordForm()

    return render(request, 'certificates/add_certificate.html', {'form': form})

def view_certificate(request, certificate_id):
    certificate = get_object_or_404(CertificateRecord, id=certificate_id)
    return render(request, 'certificates/view_certificate.html', {'certificate': certificate})

def search_certificates(request):
    query = request.GET.get('q')
    certificates = CertificateRecord.objects.filter(certificate_number__icontains=query)
    return render(request, 'certificates/certificate_list.html',{'certificates':certificates, 'query': query})

@login_required
def daily_records(request):
    daily_records = DailyRecord.objects.all().order_by('-date')
    return render(request, 'certificates/daily_records.html', {'daily_records': daily_records})

@login_required
def edit_dispatch(request, dispatch_id):
    dispatch_record = get_object_or_404(DispatchRecord, id=dispatch_id)

    if request.method == 'POST':
        form = DispatchForm(request.POST, instance=dispatch_record)
        if form.is_valid():
            form.save()
            return redirect('dispatched_certificates')
    else:
        form = DispatchForm(instance=dispatch_record)

    return render(request, 'certificates/edit_dispatch.html', {'form': form})


@login_required
def delete_dispatch(request, dispatch_id):
    dispatch_record = get_object_or_404(DispatchRecord, id=dispatch_id)

    if request.method == 'POST':
        dispatch_record.delete()
        messages.success(request, "Dispatch record deleted successfully.")
        return redirect('dispatched_certificates')

    return render(request, 'certificates/confirm_delete_dispatch.html', {'dispatch_record': dispatch_record})

@login_required
def daily_records(request):
    today = timezone.now().date()
    daily_record, created = DailyRecord.objects.get_or_create(date=today)

    context ={
        'daily_record': daily_record,
        'printed_certificates':  daily_record.printed_certificates.all(),
        'dispatched_certificates': daily_record.dispatched_certificates.all(),
    }
    return render(request, 'certificates/daily_records.html', context)