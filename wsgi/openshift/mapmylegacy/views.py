from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import RequestContext, loader
from forms import PersonSearchForm
from openshift import settings
import json
import os
import requests
import service
import urllib

FS_CLIENT_ID = settings.FS_CLIENT_ID
FS_AUTH_NETLOC = settings.FS_AUTH_NETLOC
FS_AUTH_PATH = settings.FS_AUTH_PATH
FS_TOKEN_PATH = settings.FS_TOKEN_PATH
FS_AUTH_PARAMS = settings.FS_AUTH_PARAMS 

def home(request):

    return render(request, 'home/home.html', locals())

def map(request):
    # Get the person data
    person_data = None
    form = PersonSearchForm(request.GET)
    print form
    if form.is_valid():
        # person_id = 'KWWD-HYG'
        person_id = form.cleaned_data.get('search_field')

        print person_id

        fs_access_token = service.get_access_token(request)
        if not fs_access_token:
            return redirect('/')

        person_data = service.get_person_data(fs_access_token, person_id)

        return render(request, 'home/map.html', locals())

    else:
        return redirect('/select-person')

def timeline(request):

    return render(request, 'home/timeline.html', locals())

def pedigree_match(request, person_id=None):
    fs_access_token = service.get_access_token(request)

    if not fs_access_token:
        return redirect('/')

    photos = service.get_ancestry_photos(fs_access_token, person_id)

    return render(request, 'home/pedigree-match.html', locals())

def sample_app(request):

    return render(request, 'home/sample-app.html', locals())

def logout(request):

    service.del_access_token(request)

    return render(request, 'home/home.html', locals())

def select_person(request):
    fs_access_token = service.get_access_token(request)

    if not fs_access_token:
        return redirect('/')

    curr_person_id = service.get_curr_person_data(fs_access_token, 'id')
    ancestry_json = service.get_ancestry_data(fs_access_token, curr_person_id)

    try:
        ancestry_data = json.loads(ancestry_json)
        print ancestry_data

    except ValueError:
        pass

    form = PersonSearchForm()

    return render(request, 'home/select-person.html', locals())

def custom_404(request):

    return render(request, 'home/404.html')

def custom_500(request):

    return render(request, 'home/500.html')
