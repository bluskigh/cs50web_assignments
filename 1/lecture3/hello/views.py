from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    # request reprents the http request that was made in order to access our server.
    return HttpResponse('hello there')

def name(request, name):
    return render(request, 'hello/index.html', {
        'name': name.capitalize()
    })

def greet(request, name):
    return HttpResponse('Hello, ' + name)
