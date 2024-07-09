from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.certificate_list, name='certificate_list'),
    path('dispatch/<int:certificate_id>/', views.dispatch_certificate, name='dispatch_certificate'),
    path('add/', views.add_certificate, name='add_certificate'),
    path('dispatched/', views.dispatched_certificates, name='dispatched_certificates'),
    path('', views.certificate_list, name='certificate_list'),
    path('search/', views.search_certificates, name='search_certificates'),
    path('view/<int:certificate_id>/', views.view_certificate, name='view_certificate'),
    path('print/<int:certificate_id>/', views.print_certificate, name='print_certificate'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

