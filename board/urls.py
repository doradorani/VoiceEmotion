from django.urls import path

from . import views

app_name = 'board'
urlpatterns = [
    path('', views.board_paging, name='board'),
    path('write/', views.board_write, name='write'),
    path('detail/<int:pk>/', views.board_detail, name='board_detail'),
    path('detail/edit/<int:pk>/', views.board_edit, name='edit'),
    path('notice/', views.notice_boardpaging, name='notice'),
    path('notice_detail/<int:pk>/', views.notice_detail, name='notice_detail'),
    path('mypage/', views.mypage, name='mypage'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('change_password/', views.change_password, name='change_password'),
    path('detail/delete/<int:pk>/',views.board_delete,name='delete'),
]
