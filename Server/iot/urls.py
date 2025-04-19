# web_plataform/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('lab-one/',views.lab_one, name='server-lab-one'),
    path('lab-two/',views.lab_two, name='server-lab-two'),
]