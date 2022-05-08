from django.http import HttpResponse
from django.shortcuts import render


def main(request) -> HttpResponse:
    return render(request, 'main.html', {})

def introduction(request) -> HttpResponse:
    return render(request, 'introduction.html', {})

