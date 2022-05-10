from django.http import HttpResponse
from django.shortcuts import render
from board.models import Movie

def main(request) -> HttpResponse:
    movie = Movie.objects.all()
    return render(request, 'main.html', {'movie',movie})

def introduction(request) -> HttpResponse:
    return render(request, 'introduction.html', {})

