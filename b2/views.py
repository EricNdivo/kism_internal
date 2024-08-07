from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from .models import CertificateRecord, DispatchRecord, DailyRecord
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import CertificateRecordForm, DispatchForm
from django.contrib.auth.models import User
from django.contrib import messages
from django import forms
#from .utils import send_dispatch_email
from django.conf import settings
from django.db import IntegrityError
import os
from .emails import send_dispatch_email


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
        form = CertificateRecordForm()
        return render(request, 'certificates/add_certificate.html', {'form': form})
    
@login_required
@login_required
def dispatch_certificate(request, certificate_id):
    certificate = get_object_or_404(CertificateRecord, id=certificate_id)
    
    if request.method == 'POST':
        form = DispatchForm(request.POST)
        if form.is_valid():
            dispatched_to = form.cleaned_data.get('dispatched_to')
            dispatched_phone = form.cleaned_data.get('dispatched_phone')
            picked_by_wells_fargo = form.cleaned_data.get('picked_by_wells_fargo')
            
            if dispatched_to:
                certificate.picked_by = dispatched_to
                certificate.dispatched_to = dispatched_to
            elif dispatched_phone:
                certificate.picked_by = dispatched_phone
                certificate.dispatched_phone = dispatched_phone
            elif picked_by_wells_fargo:
                certificate.picked_by = picked_by_wells_fargo
                certificate.dispatched_to = picked_by_wells_fargo
            else:
                messages.error(request, "Please provide either an email address, phone number, or select Wells Fargo.")
                return render(request, 'certificates/dispatch_certificate.html', {'certificate': certificate, 'form': form})
            
            certificate.dispatched = True
            certificate.dispatched_by = request.user
            certificate.dispatch_date = timezone.now()
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
                    dispatch_record.dispatched_to = certificate.dispatched_to
                    dispatch_record.dispatched_phone = certificate.dispatched_phone
                    dispatch_record.picked_by_wells_fargo = certificate.picked_by
                    dispatch_record.dispatch_date = timezone.now()
                    dispatch_record.save()
                
                today = timezone.now().date()
                daily_record, created = DailyRecord.objects.get_or_create(date=today)
                daily_record.dispatched_certificates.add(certificate)
                
                dispatch_records = [dispatch_record]
                
                try:
                    if dispatched_to:
                        send_dispatch_email(dispatched_to, dispatch_records)
                        print(f"Email sent to: {dispatched_to} with records: {dispatch_records}")
                    
                    messages.success(request, 'Certificate dispatched successfully.')
                    return redirect('certificate_list')

                except Exception as e:
                    messages.error(request, 'An error occurred while sending the dispatch email.')
                    print(f"Error in sending email: {e}")
                    return redirect('certificate_list')

            except IntegrityError:
                messages.error(request, 'This certificate has already been dispatched.')
                return redirect('certificate_list')
    else:
        form = DispatchForm()
    return render(request, 'certificates/dispatch_certificate.html', {'certificate': certificate, 'form': form})
@login_required
def dispatched_certificates(request):
    dispatch_records = DispatchRecord.objects.all().order_by('certificate_id')
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
def edit_dispatch(request, pk):
    dispatch_record =  DispatchRecord.objects.get(id=pk)
    form = DispatchForm(instance=dispatch_record)
    if request.method == 'POST':
        form = DispatchForm(request.POST, instance=dispatch_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Changes Updated Successfully!")
            return redirect('dispatched_certificates')
    
    context = {'form': form}
    return render(request, 'certificates/dispatch_certificate.html', context)


@login_required
def delete_dispatch(request, dispatch_id):
    dispatch_record = get_object_or_404(DispatchRecord, id=dispatch_id)

    if request.method == 'POST':
        dispatch_record.delete()
        messages.success(request, "Dispatch record deleted successfully.")
        return redirect('dispatched_certificates')

    return render(request, 'certificates/confirm_delete_dispatch.html', {'dispatch_record': dispatch_record})
