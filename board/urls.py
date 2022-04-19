from django.urls import path

from . import views

app_name = 'board'
urlpatterns = [
<<<<<<< HEAD
    path('board/', views.boardpaging, name='board'),
    path('write/',views.board_write, name = 'write'), # 게시글 작성
    path('detail/<int:pk>/',views.board_detail, name = 'board_detail'),
]
=======
    path('board/', views.board_paging, name='board'),
    path('write/', views.board_write, name='write'),
]
>>>>>>> c809c3d6f650c65c1d98f74072c5d47e8f0dfc60
