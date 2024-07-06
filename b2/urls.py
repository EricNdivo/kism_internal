from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.certificate_list, name='certificate_list'),
    path('dispatch/<int:certificate_id>/', views.dispatch_certificate, name='dispatch_certificate'),
    path('records/', views.daily_records, name='daily_records'),
    path('add/', views.add_certificate, name='add_certificate'),
    path('dispatched/', views.dispatched_certificates, name='dispatched_certificates'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
