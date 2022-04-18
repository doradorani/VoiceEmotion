from django.shortcuts import render
from django.core.paginator import Paginator
from .models import *
# Create your views here.
def boardpaging(request) : #board 간략하게 paging
    now_page = request.GET.get('page',1)
    datas = Board.objects.order_by('-id')

    p = Paginator(datas, 10)
    info = p.get_page(now_page)
    start_page = (int(now_page) - 1) // 10 * 10 + 1
    end_page = start_page + 9
    if end_page > p.num_pages:
        end_page = p.num_pages
    context = {
        'info': info,
        'page_range': range(start_page, end_page + 1)
    }
    return render(request, 'board/board.html', context)