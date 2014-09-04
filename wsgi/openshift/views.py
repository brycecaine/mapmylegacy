from django.http import HttpResponse
from django.shortcuts import render, redirect
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
    print person_response

    return render(request, 'home/map.html', locals())

def timeline(request):

    return render(request, 'home/timeline.html', locals())

def logout(request):
    template = loader.get_template('home/home.html')
    context = RequestContext(request, {})
    response = HttpResponse(template.render(context))
    fs_access_token = request.session.get('fs_access_token')
    print 'del'
    print fs_access_token

    # Delete access token
    del_acc_tok_url = '%s%s?access_token=%s' % (FS_AUTH_NETLOC, FS_TOKEN_PATH, fs_access_token)
    del_resp = requests.delete(del_acc_tok_url)
    print del_resp

    # Delete fs_access_token session variable
    del fs_access_token

    return response

def test3(request):
    return render(request, 'home/test3.html', locals())

def select_person(request):
    form = PersonSearchForm()
    response = render(request, 'home/select-person.html', locals())

    # Get access token if it exists in the session variables
    fs_access_token = request.session.get('fs_access_token')
    print 'ins'
    print fs_access_token

    # If the access token doesn't exist, have user authenticate against familysearch for it
    if fs_access_token == None:
        print 'hi'
        # Get authorization code from url
        auth_code = request.GET.get('code')

        # Get access token
        get_acc_tok_url = '%s%s' % (FS_AUTH_NETLOC, FS_TOKEN_PATH)
        get_acc_tok_data = {'grant_type': 'authorization_code',
                            'code': auth_code,
                            'client_id': FS_CLIENT_ID}
        token_response = requests.post(get_acc_tok_url, get_acc_tok_data).json()
        fs_access_token = token_response.get('access_token')

        # If response didn't contain access token, redirect to home page
        # otherwise add the access token to a session variable
        if not fs_access_token:
            return redirect('/')

        else:
            request.session.set_expiry(1800)
            request.session['fs_access_token'] = fs_access_token
            print fs_access_token
            print form

    return response

def custom_404(request):

    return render(request, 'home/404.html')

def custom_500(request):

    return render(request, 'home/500.html')
