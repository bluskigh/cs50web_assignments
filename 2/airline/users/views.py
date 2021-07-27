from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

def logout_view(request):
    return render(request, 'user_logout.html')

def login_view(request):
    return render(request, 'user_login.html')
