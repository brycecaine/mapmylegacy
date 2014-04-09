from django.shortcuts import render
import service
import settings
import urllib

FS_AUTH_NETLOC = settings.FS_AUTH_NETLOC
FS_AUTH_PATH = settings.FS_AUTH_PATH
FS_AUTH_PARAMS = settings.FS_AUTH_PARAMS 

def home(request):
    curr_person_id = service.get_curr_person_id(request)
    if curr_person_id:
        next_url = '/select-person'
        next_url_text = 'Select Ancestor'
    else:
        fs_auth_params = urllib.urlencode(FS_AUTH_PARAMS)
        fs_auth_url = '%s%s?%s' % (FS_AUTH_NETLOC,
                                   FS_AUTH_PATH,
                                   fs_auth_params)
        next_url = fs_auth_url
        next_url_text = 'Sign in using FamilySearch'

    return render(request, 'home/home.html', locals())

def select_person(request):
    curr_person_id = service.get_curr_person_id(request)
    r_ancestry_json = service.get_ancestry_data(request)

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

