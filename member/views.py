import json
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import HttpResponse, redirect, render
from django.views.decorators.csrf import csrf_exempt

from sympy import re
import pymysql
from .forms import UserForm
from .models import User

@csrf_exempt
def signup(request) -> HttpResponse:
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('main:main')
    else:
        form = UserForm()
    return render(request, 'member/signup1.html', {'form': form})

@csrf_exempt
def findId(request) -> HttpResponse:
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            m = User.objects.get(email = email)
        except User.DoesNotExist as e:
            return HttpResponse('아이디 없음')
        return HttpResponse(m.username)
    else:
        return render(request, 'member/findId.html')
@csrf_exempt
def findPwd(request) -> HttpResponse:
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        try:
            m = User.objects.get(email = email,username=username)
        except User.DoesNotExist as e:
            return HttpResponse('올바른 아이디가 아닙니다.')
        return HttpResponse(m.password)
    else:
        return render(request, 'member/findPwd.html')


# moviedict = {
#         'image': movie.image
#     }
#     movieJson = json.dumps(moviedict)
#     return render(request, 'signup2.html', {'movieJson': movieJson})   


def rating(request) -> HttpResponse:
    db = pymysql.connect(user = 'root', host = '192.18.138.86', passwd = '5631jjyy', port = 3306, db = 'jango_db')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT img FROM movies"
    cursor.execute(sql)
    movieJson = json.dumps(cursor.fetchall())
    username = request.user.id
    response = render(request, 'member/rating.html', {'movieJson':movieJson})
    response.set_cookie('user_id',username)
    return response