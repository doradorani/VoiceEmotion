import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def service(request) -> HttpResponse:
    return render(request, "index.html", {})