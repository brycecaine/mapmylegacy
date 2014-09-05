from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext, loader
from forms import PersonSearchForm
import json
import os
import requests
import service
import settings
import urllib

FS_CLIENT_ID = settings.FS_CLIENT_ID
FS_AUTH_NETLOC = settings.FS_AUTH_NETLOC
FS_AUTH_PATH = settings.FS_AUTH_PATH
FS_TOKEN_PATH = settings.FS_TOKEN_PATH
FS_AUTH_PARAMS = settings.FS_AUTH_PARAMS 
FS_PERSON_PATH = settings.FS_PERSON_PATH 

def home(request):

    return render(request, 'home/home.html', locals())

def map(request):
    # Get the person data
    person_id = 'KW71-481'
    get_person_url = '%s%s%s' % (FS_AUTH_NETLOC, FS_PERSON_PATH, person_id)
    get_person_headers = {'Accept': 'application/x-gedcomx-v1+json',
                          'Authorization': 'Bearer ' + fs_access_token}
    person_response = requests.get(get_person_url, headers=get_person_headers).json()

    return render(request, 'home/map.html', locals())

def timeline(request):

    return render(request, 'home/timeline.html', locals())

def logout(request):

    service.del_access_token(request)

    return render(request, 'home/home.html', locals())

def select_person(request):
    fs_access_token = service.get_access_token(request)
    curr_person_id = service.get_curr_person_data(fs_access_token, 'id')
    ancestry_json = service.get_ancestry_data(fs_access_token, curr_person_id)
    ancestry_data = json.loads(ancestry_json)
    print ancestry_data
    form = PersonSearchForm()

    return render(request, 'home/select-person.html', locals())

def custom_404(request):

    return render(request, 'home/404.html')

def custom_500(request):

    return render(request, 'home/500.html')
