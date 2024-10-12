from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', views.login, name='login'),
    path('register', views.Register.as_view() , name='register'),
    path('settings/change_password/', auth_views.PasswordChangeView.as_view(template_name='auth/change_password.html'), name='change_password'),
    path('settings/change_password/success/', auth_views.PasswordChangeDoneView.as_view(template_name='auth/change_password_success.html'), name='password_change_done'),
    path('logout', views.logout, name='logout'),
]