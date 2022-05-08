from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('main/', views.main, name='main'),
    path('introduction/', views.introduction, name='introduction'),
]
