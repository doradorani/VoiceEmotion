from django.http import HttpResponse
from django.shortcuts import render
from board.models import Movie

def main(request) -> HttpResponse:
    movie = Movie.objects.order_by('movieId')
    context = {'movie':movie}
    return render(request, 'main.html', context)

def introduction(request) -> HttpResponse:
    return render(request, 'introduction.html', {})

