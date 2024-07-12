from django.test import TestCase, Client
from django.urls import reverse
from .models import CertificateRecord, DispatchRecord, DailyRecord
from django.contrib.auth.models import User
from datetime import datetime

class CertificateTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_certificate_list(self):
        response = self.client.get(reverse('certificate_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'certificates/certificate_list.html')

    def test_add_certificate(self):
        response = self.client.post(reverse('add_certificate'), {
            'certificate_number': '12345',
            'uploaded_certificate': 'path/to/certificate.pdf'
        })
        self.assertEqual(response.status_code, 302)  
        
    def test_search_certificates_found(self):
        CertificateRecord.objects.create(certificate_number='12345', uploaded_certificate='path/to/certificate.pdf')
        response = self.client.get(reverse('search_certificates'), {'q': '12345'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '12345')

    def test_search_certificates_not_found(self):
        response = self.client.get(reverse('search_certificates'), {'q': 'notfound'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Certificate Not Found')

    def test_daily_records(self):
        response = self.client.get(reverse('daily_records'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'certificates/daily_records.html')

    def test_dispatch_certificate_invalid(self):
        certificate = CertificateRecord.objects.create(certificate_number='12345', uploaded_certificate='path/to/certificate.pdf')
        response = self.client.post(reverse('dispatch_certificate', args=[certificate.id]), {})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please provide either an email address, phone number, or select Wells Fargo.')

    def test_delete_dispatch(self):
        certificate = CertificateRecord.objects.create(certificate_number='12345', uploaded_certificate='path/to/certificate.pdf')
        dispatch_record = DispatchRecord.objects.create(certificate=certificate, dispatched_by=self.user, dispatch_date=datetime.now())
        url = reverse('delete_dispatch', args=[dispatch_record.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302) 
        self.assertFalse(DispatchRecord.objects.filter(id=dispatch_record.id).exists())

