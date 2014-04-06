import os
from django.shortcuts import render

def home(request):
    return render(request, 'home/home.html', locals())

def select_person(request):

    return render(request, 'home/select-person.html', locals())

def map(request):

    return render(request, 'home/map.html', locals())

def timeline(request):

    return render(request, 'home/timeline.html', locals())

def custom_404(request):
    return render(request, 'home/404.html')

def custom_500(request):
    return render(request, 'home/500.html')

