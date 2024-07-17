from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from .models import CertificateRecord, DispatchRecord, DailyRecord
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import CertificateRecordForm, DispatchForm
from django.contrib.auth.models import User
from django.contrib import messages
from django import forms
from .utils import send_dispatch_email
from django.conf import settings
from django.db import IntegrityError
import os

@login_required
def certificate_list(request):
    certificates = CertificateRecord.objects.all()
    return render(request, 'certificates/certificate_list.html', {'certificates': certificates})

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
            certificate.dispatched_to = picked_by_email
            certificate.dispatch_date = timezone.now()
            certificate.dispatched_phone = picked_by_phone
            certificate.save()

            try:
                dispatch_record, created = DispatchRecord.objects.get_or_create(
                    certificate=certificate,
                    defaults={
                        'dispatched_by': request.user,
                        'dispatched_phone': certificate.dispatched_phone,
                        'dispatched_to': certificate.dispatched_to,
                        'dispatch_date': timezone.now()
                    }
                )
                
                if not created:
                    dispatch_record.dispatched_by = request.user
                    dispatch_record.dispatched_phone = certificate.dispatched_phone
                    dispatch_record.dispatch_date = timezone.now()
                    dispatch_record.save()
            
                today = timezone.now().date()
                daily_record, created = DailyRecord.objects.get_or_create(date=today)
                daily_record.dispatched_certificates.add(certificate)
                
                
                dispatch_records = [dispatch_record]
                if picked_by_email:
                    send_dispatch_email(picked_by_email, dispatch_records)
                
                messages.success(request, 'Certificate dispatched successfully.')
                return redirect('certificate_list')
            except IntegrityError:
                messages.error(request, 'This certificate has already been dispatched.')
                return redirect('certificate_list')
    else:
        form = DispatchForm()
    
    return render(request, 'certificates/dispatch_certificate.html', {'certificate': certificate, 'form': form})

@login_required
def dispatched_certificates(request):
    dispatch_records = DispatchRecord.objects.all()
    return render(request, 'certificates/dispatched_certificates.html', {'dispatch_records': dispatch_records})


def view_certificate(request, certificate_id):
    certificate = get_object_or_404(CertificateRecord, id=certificate_id)
    return render(request, 'certificates/view_certificate.html', {'certificate': certificate})

def search_certificates(request):
    query = request.GET.get('q')
    certificates = CertificateRecord.objects.filter(certificate_number__icontains=query)
    
    if not certificates:
        messages.error(request, f'Certificate Not Found.', query)
        
    return render(request, 'certificates/certificate_list.html', {'certificates': certificates, 'query': query})

def search_dispatched_certificates(request):
    query = request.GET.get('q')

    dispatch_records = DispatchRecord.objects.filter(
        certificate__certificate_number__icontains=query
    )
    context = {
        'dispatch_records': dispatch_records,
        'query': query,
    }

    if not dispatch_records:
        messages.error(request, f'Certificate Not Found.', query)
       
    return render(request, 'certificates/dispatched_certificates.html', context)

def search_daily_records(request):
    query = request.GET.get('q', '').strip()
    if query:
        daily_records = DailyRecord.objects.filter(
            dispatched_certificates__certificate_number__icontains=query
        ).distinct()
        debug_info= f"Query: {query}, Found records: {daily_records.count()}"
    else:
        daily_records = DailyRecord.objects.none()
        debug_info = "No query provided."   
    context = {
        'daily_records': daily_records,
        'query': query,
        'debug_info': debug_info,
    } 
    if not daily_records:
        messages.error(request, f'Certificate Not Found', query)

    return render(request, 'certificates/daily_records.html', context)

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

