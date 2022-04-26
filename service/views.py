import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def service(request) -> HttpResponse:
    return render(request, 'service.html', {})

def chat(request):
    return render(request, 'service/chat.html')

@csrf_exempt
def chatbot(request):
    get_data = json.loads(request.body.decode('utf-8'))
    print(get_data['message'])
    data = {
        'message':'안녕하세요.'

    }
    return JsonResponse(data)