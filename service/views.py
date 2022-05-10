from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def service(request) -> HttpResponse:
    username = request.user.id
    response = render(request, "index.html", {})
    response.set_cookie('user_id',username)
    return response
    