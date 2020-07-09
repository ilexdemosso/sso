from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('authorize', views.authorize, name='authorize'),
    path('error', views.error, name='error')
]