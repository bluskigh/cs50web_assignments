from django.shortcuts import render, redirect
from django.http import HttpResponse

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry_title):
    information = util.get_entry(entry_title)
    if information is None:
        return render(request, 'encyclopedia/error.html', {'error': 'Entry Not Found', 'description': 'Could not find any information regarding "' + entry_title + '"'})
    return render(request, 'encyclopedia/entry.html', {
        'information': information
    })
