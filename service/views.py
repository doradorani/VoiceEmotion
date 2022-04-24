from django.http import HttpResponse
from django.shortcuts import render


def service(request) -> HttpResponse:
    return render(request, 'service.html', {})
