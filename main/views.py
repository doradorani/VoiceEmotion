from django.http import HttpResponse
from django.shortcuts import render


def main(request) -> HttpResponse:
    return render(request, 'main.html', {})
