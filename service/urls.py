from django.urls import path

from . import views

app_name = 'service'

urlpatterns = [
    path('service/', views.service, name='service'),
    path('service/test', views.test, name='test'),
]
