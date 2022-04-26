from django.urls import path

from . import views

app_name = 'service'

urlpatterns = [
    path('service/', views.service, name='service'),
    path('service/chat', views.chat, name='chat'),
    path('service/chatbot', views.chatbot, name='chatbot'),

]
