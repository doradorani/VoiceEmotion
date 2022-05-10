from django.http import HttpResponse
from django.shortcuts import render
from board.models import Movie

def main(request) -> HttpResponse:
    datas = Movie.objects.order_by('movieId')
    return render(request, 'main.html', {'movie',datas})

def introduction(request) -> HttpResponse:
    return render(request, 'introduction.html', {})

