from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return HttpResponse(f'Logged in as: {request.user.username}. <br> To signout go to route: /logout')
    return HttpResponse('Not Logged in, go to route: /login')

# why am I like this.
def login_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            # user = index according to the urls.py
            return redirect(index)
        else:
            return HttpResponse('Could not log you in, return to route: /login')
    return render(request, 'users/login.html')

# bruh... silly mistake made, I named logout_view logout....
def logout_view(request):
    logout(request)
    return redirect(index)
