<<<<<<< HEAD
from django.shortcuts import render,redirect, get_object_or_404
=======
from django.contrib.auth.decorators import login_required
>>>>>>> c809c3d6f650c65c1d98f74072c5d47e8f0dfc60
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
<<<<<<< HEAD
from .forms import BoardWriteForm, CommentForm
from django.contrib.auth.decorators import login_required
=======

from .forms import BoardWriteForm
>>>>>>> c809c3d6f650c65c1d98f74072c5d47e8f0dfc60
from .models import *


def board_paging(request):
    """Simple Board Paging."""
    now_page = request.GET.get('page', 1)
    datas = Board.objects.order_by('-id')

    p = Paginator(datas, 10)
    info = p.get_page(now_page)
    start_page = (int(now_page) - 1) // 10 * 10 + 1
    end_page = start_page + 9
    if end_page > p.num_pages:
        end_page = p.num_pages
    context = {'info': info, 'page_range': range(start_page, end_page + 1)}
    return render(request, 'board/board.html', context)


@csrf_exempt
@login_required
def board_write(request):
    """Write New Posts."""
    if request.method == 'POST':
        form = BoardWriteForm(request.POST, request.FILES)
        if form.is_valid():
            writing = form.save(commit=False)
            writing.user = request.user
            writing.save()
            return redirect('board:board')
    else:
        form = BoardWriteForm()

    context = {'form': form}
    return render(request, 'board/write.html', context)
<<<<<<< HEAD
@csrf_exempt
def board_detail(request, pk):
    board = get_object_or_404(Board, pk=pk)
    comments = Comment.objects.filter(board = pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.board = board
            comment.author = request.user
            comment.save()
            return redirect('board:board_detail', pk)
    else:
        form = CommentForm()
    
    context = {
        'form' : form,
        'board': board,
        'comments':comments,
        'pk':pk
    }

    return render(request, 'board/detail.html', context)
@csrf_exempt
def board_detail(request, pk):
    board = get_object_or_404(Board, pk=pk)
    comments = Comment.objects.filter(board = pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.board = board
            comment.author = request.user
            comment.save()
            return redirect('board:board_detail', pk)
    else:
        form = CommentForm()
    
    context = {
        'form' : form,
        'board': board,
        'comments':comments,
        'pk':pk
    }
    board.hit_cnt += 1
    board.save()

    return render(request, 'board/detail.html', context)
=======
>>>>>>> c809c3d6f650c65c1d98f74072c5d47e8f0dfc60
