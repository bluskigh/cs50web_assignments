from time import sleep
from random import randint

from django.http import HttpResponse, Http404, JsonResponse 
from django.shortcuts import render

texts = ['first 1', 'second 2', 'third 3']


# Create your views here.
def index(request):
    return render(request, 'main/index.html')


def sections(request, section_id):
    if section_id >= 1 and section_id <= 3:
        return HttpResponse(texts[section_id-1])
    else:
        raise Http404('Invalid section id')


def items(request):
    # start is required
    start = request.GET.get('start') or 0
    # by default will be fetching 10 items
    end = request.GET.get('end') or (start + 10)
    item_list = []
    for i in range(int(start), int(end)):
        final = ""
        for i in range(randint(10, 20)):
            final += chr(randint(97, 122))
        item_list.append(final)
    # sleep a second
    sleep(1)
    return JsonResponse(item_list, safe=False)


