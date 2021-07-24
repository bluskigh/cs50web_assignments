from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('name/<str:name>', views.name, name='name'),
    path('<str:name>', views.greet, name='greet')

]
