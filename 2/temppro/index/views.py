from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Todo 
from django import forms 

class TodoForm(forms.Form):
    title = forms.CharField(max_length=64)
    description = forms.CharField(max_length=64)

# Create your views here.
def index(request):
    form = TodoForm()
    return render(request, 'index/home.html', {'todos': Todo.objects.all(),
        'form': form})

def todos(request):
    if request.method == 'POST':
        # fill form properties with the POST values
        form = TodoForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Todo.objects.create(title=cd.get('title'), 
                    description=cd.get('description'))
            # using name given to the index path in urls.py
            return redirect('index')
        # form is not valid, return form in context to display errors
        return HttpResponse(request, 'index/home.html', {'form': form})

def delete_todo(request):
    if request.method == 'POST':
        _id = request.POST.get('id')
        temp = Todo.objects.get(id=_id)
        if temp is None:
            return HttpResponse('invalid id')
        temp.delete()
    print(request.method)
    return redirect('index')
