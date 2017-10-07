from django.conf.urls import url, include
from . import views
#Importación de vistas de contrib.auth de django
from django.contrib.auth import views as auth_views

app_name = 'cuentas'

urlpatterns = [
    #cuentas/
    url(r'^login/$', auth_views.LoginView.as_view(template_name='cuentas/login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='cuentas/logout.html'), name="logout"),
    url(r'^password_change/$',auth_views.PasswordChangeView.as_view(template_name='change-password.html'), name='password-change'),
    url(r'^password_change/done/$', auth_views.PasswordChangeDoneView.as_view(template_name='change-password-done.html'), name='password-change-done'),
    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(template_name='password-reset.html'), name='password-reset'),
    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(template_name='password-reset.html'), name='password-reset-done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.PasswordResetConfirmView.as_view(
        template_name='password-reset-confirm.html'), name='reset'),
    url(r'^reset/done/$', auth_views.PasswordResetConfirmView.as_view(template_name='password-reset-done.html'), name='reset-done'),
    url(r'^registrar/$', views.registrar, name="registrar"),
]
