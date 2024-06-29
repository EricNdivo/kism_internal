from django.urls import path
from . import views

urlpatterns = [
    path('', views.certificate_list, name='certificate_list'),
    path('dispatch/<int:certificate_id>/', views.dispatch_certificate, name='dispatch_certificate'),
    path('records/', views.daily_records, name='daily_records'),
    path('add/', views.add_certificate, name='add_certificate'),
]
