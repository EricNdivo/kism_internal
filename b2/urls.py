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
    path('certificates/daily-records/', views.daily_records, name='daily_records'),
    path('dispatch/edit/<str:pk>/', views.edit_dispatch, name='edit_dispatch'),
    path('dispatch/delete/<int:dispatch_id>/', views.delete_dispatch, name='delete_dispatch'),
    path('search-dispatched-certificates/', views.search_dispatched_certificates, name='search_dispatched_certificates'),
    path('search_daily_records', views.search_daily_records, name='search_daily_records'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

