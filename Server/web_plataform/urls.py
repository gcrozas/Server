# web_plataform/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='server-home'),
    path('about/',views.about, name='server-about'),
    path('backup/',views.backup, name='server-backup'),
    path('export_excel',views.export_excel,
         name='export-excel'),
]