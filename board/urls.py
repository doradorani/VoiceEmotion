from django.urls import path

from . import views

app_name = 'board'
urlpatterns = [
    path('board/', views.boardpaging, name='board'),
    path('write/', views.board_write, name='write'),
    path('detail/<int:pk>/', views.board_detail, name='board_detail'),
]
