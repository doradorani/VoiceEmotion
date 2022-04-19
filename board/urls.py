from django.urls import path

from . import views

app_name = 'board'
urlpatterns = [
    path('board/', views.board_paging, name='board'),
    path('write/', views.board_write, name='write'),
]
