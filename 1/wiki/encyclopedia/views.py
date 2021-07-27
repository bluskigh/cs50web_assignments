from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
from random import randint
from . import util
import markdown2

class NewPageForm(forms.Form):
    title = forms.CharField(label='Title')
    markdown = forms.CharField(label='Markddown', widget=forms.Textarea(attrs={'rows': 5, 'cols': 20}))

    # using clean method to add custom errors
    def clean(self):
        # cd = cleaned data
        cd = self.cleaned_data
        title = cd.get('title')
        if util.get_entry(title) is not None:
            self.add_error('title', f'A title of "{title}" aldreay exist.')
        return cd

class EditPageForm(forms.Form):
    markdown = forms.CharField(label='Markdown', min_length=5, widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry_title):
    information = util.get_entry(entry_title)
    if information is None:
        return render(request, 'encyclopedia/error.html', {'error': 'Entry Not Found', 'description': 'Could not find any information regarding "' + entry_title + '"'})
    return render(request, 'encyclopedia/entry.html', {
        'information': markdown2.markdown(information),
        'entry_title': entry_title
    })

def search(request):
    title = request.GET.get('q')
    information = util.get_entry(title)
    # could not find any entries with the exact title
    if information is None:
        # return all the entries that contain the title characters in order
        return render(request, "encyclopedia/search_result.html", {
            'title': title,
            "entries": util.contains_characters(title)
        })
    return redirect(entry, entry_title=title)
        
def new_page(request):
    if request.method == 'GET':
        return render(request, 'encyclopedia/form_layout.html', {
            'form': NewPageForm(),
            'title': 'New Page',
            'action': '/new_page',
            'header': 'New Page'
        })
    elif request.method == 'POST':
        # filling the forms properties with the values given to the request
        form = NewPageForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            title = cd.get('title')
            markdown = cd.get('markdown')
            print(markdown)
            # saving the page
            util.save_entry(title, markdown)
            # redirecting the user to the new entry page
            return redirect(entry, entry_title=title)
        else:
            # rendering page so the error is shown to the user
            return render(request, 'encyclopedia/form_layout.html', {
                'form': form,
                'title': 'New Page',
                'action': '/new_page',
                'header': 'New Page'
            })

def edit(request, entry_title):
    if request.method == 'GET':
        form = EditPageForm()
        # populating the markdown entry_title with the markdown of the entry_title the user is attempting to edit
        form.fields['markdown'].initial = util.get_entry(entry_title)
        # rendering the edit page to the user
        return render(request, 'encyclopedia/form_layout.html', { 'form': form, 'title': 'Edit Page | WiKi', 'action': '/edit', 'header': 'Edit Page'})
    elif request.method == 'POST':
        form = EditPageForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # by saving with an existing entry title, util.save_entry will delete the existing one and replace with new markdown thus "editing" the entry.
            util.save_entry(entry_title, cd.get('markdown'))
            # redirecting the newly edited entry page
            return redirect(entry, entry_title=entry_title)

def random(request):
    entries = util.list_entries()
    return redirect(entry, entry_title=entries[randint(0, len(entries)-1)])
