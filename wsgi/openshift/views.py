from django.shortcuts import render
import service
import settings
import urllib

FS_AUTH_NETLOC = settings.FS_AUTH_NETLOC
FS_AUTH_PATH = settings.FS_AUTH_PATH
FS_AUTH_PARAMS = settings.FS_AUTH_PARAMS 

def home(request):

    return render(request, 'home/home.html', locals())

def select_person(request):
    fs_access_token = service.get_access_token(request)
    print fs_access_token
    return render(request, 'home/select-person.html', locals())

def map(request):

    return render(request, 'home/map.html', locals())

def timeline(request):

    return render(request, 'home/timeline.html', locals())

def logout(request):
    # Delete the access token
    return render(request, 'home/home.html', locals())

def custom_404(request):
    return render(request, 'home/404.html')

def custom_500(request):
    return render(request, 'home/500.html')

