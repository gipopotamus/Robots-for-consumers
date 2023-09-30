from django.urls import path
from . import services

urlpatterns = [
    path('report/', services.generate_excel_report, name='download_excel_report'),
]
