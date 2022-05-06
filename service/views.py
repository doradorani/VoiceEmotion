import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

@login_required
def service(request) -> HttpResponse:
    username = request.user.id
    response = render(request, "index.html", {})
    response.set_cookie('user_id',username)
    return response
    