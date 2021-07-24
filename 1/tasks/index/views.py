from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from json import load

class NewTaskForm(forms.Form):
    task = forms.CharField(label='New Task')

# Create your views here.
def index(request):
    if 'taskitems' not in request.session:
        request.session['taskitems'] = []
        request.session['doneitems'] = []
    print(request.session.get('taskitems'))
    return render(request, 'index/home.html', {
        'tasks': request.session.get('taskitems'),
        'done': request.session.get('doneitems'),
        'form': NewTaskForm()
    })

def tasks(request):
    if request.method == "POST":
        task = request.POST.get('task')
        # popping or calling any function on this does not seem to be working, perhaps assign the value to be something else each time temp the current value perform operating tyhen assign again.
        request.session['taskitems'] += [task]
    return redirect(index)
    # return JsonResponse({'success': False}) 

def done(request):
    if request.method == 'POST':
        # have to load the AJAX request into our view
        task = load(request).get('task')
        request.session['taskitems'].pop(request.session.get('taskitems').index(task))
        request.session['doneitems'].append(task)
        return JsonResponse({'success': True})
    return redirect(index)
