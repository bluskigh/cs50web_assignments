from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/new_page', views.new_page, name='new_page'),
    path('wiki/search', views.search, name='search'),
    path('wiki/<str:entry_title>', views.entry, name='entry'),
    path('wiki/edit/<str:entry_title>', views.edit, name='edit'),
    path('random', views.random, name='random')
]
