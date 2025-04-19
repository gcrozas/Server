# Server/urls.py
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from iot import views as iot_views
from iot.admin import server_site


urlpatterns = [
    path('admin/', server_site.urls),
    path('register/',user_views.register,name='server-register'),
    path('profile/',user_views.profile,name='server-profile'),
    path('lab-one/',iot_views.lab_one, name='server-lab-one'),
    path('lab-two/',iot_views.lab_two, name='server-lab-two'),
    path('login/',auth_views.LoginView.as_view(template_name='login.html'),name='server-login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='logout.html'),name='server-logout'),
    path('', include('web_plataform.urls')), #Pagina principal
] + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)