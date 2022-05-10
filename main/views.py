from django.http import HttpResponse
from django.shortcuts import render
from board.models import Movie,Ratings

def main(request) -> HttpResponse:
    movie = Movie.objects.order_by('movieId')[:10]
    rating = Ratings.objects.raw('SELECT avg(rating) as avg FROM Ratings GROUP BY movieId ORDER BY movieId ASC')
    context = {'movie':movie,'rating':rating}
    return render(request, 'main.html', context)

def introduction(request) -> HttpResponse:
    return render(request, 'introduction.html', {})

