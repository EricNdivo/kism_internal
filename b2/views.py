from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from .models import CertificateRecord, DailyRecord, DispatchRecord
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import CertificateRecordForm 

@login_required
def certificate_list(request):
    certificates = CertificateRecord.objects.all()
    return render(request, 'certificates/certificate_list.html', {'certificates': certificates})

'''@login_required
def dispatch_certificate(request, certificate_id):
    certificate = get_object_or_404(CertificateRecord, id=certificate_id)
    
    if request.method == 'POST':
        certificate.dispatched = True
        certificate.dispatched_by = request.user
        certificate.dispatch_date = timezone.now()
        certificate.picked_by = request.POST.get('picked_by')
        certificate.save()

        daily_record, created = DailyRecord.objects.get_or_create(date=timezone.now().date())
        daily_record.dispatched_certificates.add(certificate)

        return redirect('certificate_list')

    return render(request, 'certificates/dispatch_certificate.html', {'certificate': certificate})'''

@login_required
def daily_records(request):
    records = DailyRecord.objects.all()
    return render(request, 'certificates/daily_records.html', {'records': records})

@login_required
def add_certificate(request):
    if request.method == 'POST':
        form = CertificateRecordForm(request.POST)
        if form.is_valid():
            certificate = form.save(commit=False)
            certificate.printed_by = request.user
            certificate.save()
            return redirect('certificate_list')
    else:
        form = CertificateRecordForm()
    return render(request, 'certificates/add_certificate.html', {'form': form})


@login_required
def dispatch_certificate(request, certificate_id):
    certificate = get_object_or_404(CertificateRecord, id=certificate_id)
    
    if request.method == 'POST':
        certificate.dispatched = True
        certificate.dispatched_by = request.user
        certificate.dispatch_date = timezone.now()
        certificate.picked_by = request.POST.get('picked_by')
        certificate.save()
        
        dispatch_record = DispatchRecord(certificate=certificate, dispatched_by=request.user, dispatch_date=timezone.now())
        dispatch_record.save()
        
        daily_record, created = DailyRecord.objects.get_or_create(date=timezone.now().date())
        daily_record.dispatched_certificates.add(certificate)
        
        return redirect('certificate_list')
    
    return render(request, 'certificates/dispatch_certificate.html', {'certificate': certificate})

@login_required
def dispatched_certificates(request):
    dispatch_records = DispatchRecord.objects.all()
    return render(request, 'certificates/dispatched_certificates.html', {'dispatch_records': dispatch_records})
