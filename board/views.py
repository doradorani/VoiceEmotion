from django.db.models import Avg
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import check_password
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from matplotlib.style import context
from sympy import re

from .forms import BoardWriteForm, CommentForm, BoardEditForm,RatingForm
from .models import Board, Comment, Notice,Movie,Ratings
from member.models import User

@csrf_exempt
@login_required
def board_write(request) -> HttpResponse:
    """Write New Posts."""
    if request.method == 'POST':
        form = BoardWriteForm(request.POST, request.FILES)

        if form.is_valid():
            writing = form.save(commit=False)
            writing.user = request.user
            writing.save()

            return redirect('board:mypage')
    else:
        form = BoardWriteForm()

    context = {'form': form}

    return render(request, 'board/write.html', context)


@csrf_exempt
def board_detail(request, pk) -> HttpResponse:
    """TODO board detail???"""
    board = get_object_or_404(Board, pk=pk)
    comments = Comment.objects.filter(board=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            _comment = form.save(commit=False)
            _comment.board = board
            _comment.author = request.user
            _comment.save()

            return redirect('board:board_detail', pk)
    else:
        form = CommentForm()

    context = {'form': form, 'board': board, 'comments': comments, 'pk': pk}
    board.save()

    return render(request, 'board/detail.html', context)


@csrf_exempt
@login_required
def comment(request, board_id) -> HttpResponse:
    """Excpect as Comment"""
    board = get_object_or_404(Board, pk=board_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            _comment = form.save(commit=False)
            _comment.author = request.user
            _comment.board = board
            _comment.save()
            return redirect('board:detail', board_id=board_id)
    else:
        form = CommentForm()

    context = {'board': board, 'form': form}

    return render(request, 'board:detail', context)


@csrf_exempt
@login_required
def board_edit(request, pk) -> HttpResponse:
    # NOTE Better move to top. This function is seprate by `comment()`
    """TODO Expect as Edit private board"""
    board = Board.objects.get(id=pk)
    if request.method == 'POST':
        form = BoardEditForm(request.POST)
        if form.is_valid():
            board.title = request.POST['title']
            board.content = request.POST['content']
            board.save()
            return redirect('board:board_detail',pk)
    else:
        form = BoardWriteForm(instance=board)

        return render(request, 'board/edit.html', {'form':form})


@csrf_exempt
def notice_boardpaging(request):
    now_page = request.GET.get('page', 1)
    datas = Notice.objects.all().order_by('-id')

    p = Paginator(datas, 10)
    info = p.get_page(now_page)
    start_page = (int(now_page) - 1) // 10 * 10 + 1
    end_page = start_page + 9
    if end_page > p.num_pages:
        end_page = p.num_pages
    context = {'info': info, 'page_range': range(start_page, end_page + 1)}
    return render(request, 'board/notice.html', context)


@csrf_exempt
def notice_detail(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    context = {
        'notice': notice,
    }

    return render(request, 'board/notice_detail.html', context)


@login_required
def mypage(request):
    now_page = request.GET.get('page', 1)
    user = request.user
    datas = Board.objects.filter(user_id=user).order_by('-id')

    paginator = Paginator(datas, 10)
    info = paginator.get_page(now_page)
    start_page = (int(now_page) - 1) // 10 * 10 + 1
    end_page = start_page + 1

    if end_page > paginator.num_pages:
        end_page = paginator.num_pages

    context = {'info': info, 'page_range': range(start_page, end_page + 1)}
    return render(request, 'board/mypage.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('board:mypage')
    else:
        form = PasswordChangeForm(request.user)

    context = {
        'form': form,
    }

    return render(request, 'board/change_password.html', context)


@csrf_exempt
@login_required
def withdraw(request):
    if request.method == 'POST':
        password = request.POST.get('password', '')
        user = request.user
        if check_password(password, user.password):
            user.delete()
            return redirect('/main/')

    return render(request, 'board/withdraw.html')

@login_required
def board_delete(request,pk):
    board = get_object_or_404(Board, pk=pk)
    board.delete()
    return redirect('board:mypage')

def movieReview(request) -> HttpResponse:
    """Simple Board Paging."""
    now_page = request.GET.get('page', 1)
    datas = Movie.objects.order_by('movieId')

    p = Paginator(datas, 10)
    info = p.get_page(now_page)
    start_page = (int(now_page) - 1) // 10 * 10 + 1
    end_page = start_page + 9

    if end_page > p.num_pages:
        end_page = p.num_pages
    context = {'info': info, 'page_range': range(start_page, end_page + 1)}
    return render(request,'board/review.html',context)

@csrf_exempt
def reviewDetail(request, pk) -> HttpResponse:
    """TODO board detail???"""
    movie = get_object_or_404(Movie, pk=pk)
    ratings = Ratings.objects.filter(movieId=pk)
    rating_avg = Ratings.objects.filter(movieId=pk).aggregate(Avg('rating'))
    if request.method == 'POST':
        form = RatingForm(request.POST)

        if form.is_valid():
            _rating = form.save(commit=False)
            _rating.movieId = movie.movieId
            _rating.userid = request.user
            _rating.save()

            return redirect('board:reviewDetail', pk)
    else:
        form = RatingForm()

    context = {'form': form, 'movie': movie, 'ratings': ratings, 'pk': pk ,'rating_avg':rating_avg}
    movie.save()

    return render(request, 'board/reviewDetail.html', context)

@csrf_exempt
@login_required
def comment(request, movie_id) -> HttpResponse:
    """Excpect as Comment"""
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == 'POST':
        form = RatingForm(request.POST)

        if form.is_valid():
            _rating = form.save(commit=False)
            _rating.userid = request.user
            _rating.movieId = movie.movieId
            _rating.save()
            return redirect('board:reviewDetail', movie_id=movie_id)
    else:
        form = RatingForm()

    context = {'movie': movie, 'form': form}

    return render(request, 'board:reviewDetail', context)