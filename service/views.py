from django.http import HttpResponse
from django.shortcuts import render


def service(request) -> HttpResponse:
    return render(request, 'service.html', {})

def test(request) -> HttpResponse:
    return render(request, 'service/service_test.html', {})
