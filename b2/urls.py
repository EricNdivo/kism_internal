from django.urls import path
from . import views

urlpatterns = [
    path('', views.certificate_list, name='certificate_list'),
    path('dispatch/<int:certificate_id>/', views.dispatch_certificate, name='dispatch_certificate'),
    path('records/', views.daily_records, name='daily_records'),
    path('add/', views.add_certificate, name='add_certificate'),
    path('dispatched/', views.dispatched_certificates, name='dispatched_certificates'),
    path('', views.certificate_list, name='certificate_list'),
    path('search/', views.search_certificates, name='search_certificates'),
    path('view/<int:certificate_id>/', views.view_certificate, name='view_certificate'),
    path('print/<int:certificate_id>/', views.print_certificate, name='print_certificate'),
]
