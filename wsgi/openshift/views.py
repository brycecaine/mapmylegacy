from django.shortcuts import render
import json
import os
import requests
import urllib

FS_CLIENT_ID = 'WCQY-7J1Q-GKVV-7DNM-SQ5M-9Q5H-JX3H-CMJK'
FS_AUTH_NETLOC = 'https://sandbox.familysearch.org'
FS_AUTH_PATH = '/cis-web/oauth2/v3/authorization'
FS_AUTH_PARAMS = \
    {'redirect_uri': 'http://localhost:3000/select-person',
     'response_type': 'code',
     'client_id': FS_CLIENT_ID}

FS_TOKEN_PATH = '/cis-web/oauth2/v3/token'
FS_TOKEN_PARAMS = \
    {'grant_type': 'authorization_code',
     'client_id': FS_CLIENT_ID}

FS_NETLOC = 'https://sandbox.familysearch.org'

def home(request):
    fs_auth_params = urllib.urlencode(FS_AUTH_PARAMS)
    fs_auth_url = '%s%s?%s' % (FS_AUTH_NETLOC,
                               FS_AUTH_PATH,
                               fs_auth_params)

    return render(request, 'home/home.html', locals())

def select_person(request):
    # -------------------------------------------------------------------------
    # Get access token
    fs_token_url = '%s%s' % (FS_AUTH_NETLOC, FS_TOKEN_PATH)
    fs_auth_code = request.GET.get('code')
    fs_token_params = FS_TOKEN_PARAMS
    fs_token_params['code'] = fs_auth_code
    fs_token_params_json = json.dumps(fs_token_params)
    fs_token_headers = {'content-type': 'application/json'}
    
    r_auth = requests.post(fs_token_url, data=fs_token_params)
    fs_access_token = r_auth.json()['access_token']

    # -------------------------------------------------------------------------
    # Get current person id
    fs_person_path = '/platform/users/current.json'
    fs_person_url = '%s%s' % (FS_NETLOC, fs_person_path)
    fs_auth_headers = {'Authorization': 'Bearer %s' % fs_access_token}
    r_person = requests.get(fs_person_url, headers=fs_auth_headers)
    r_person_json = r_person.text
    r_person_dict = json.loads(r_person_json)
    curr_person_id = r_person_dict['users'][0]['personId']

    # -------------------------------------------------------------------------
    # Get ancestry data
    fs_ancestry_path = '/platform/tree/ancestry.json'
    fs_ancestry_url = '%s%s' % (FS_NETLOC, fs_ancestry_path)
    fs_ancestry_params = {'person': curr_person_id}
    fs_ancestry_params_json = json.dumps(fs_ancestry_params)
    fs_auth_headers = {'Authorization': 'Bearer %s' % fs_access_token}
    # r_ancestry = requests.get(fs_ancestry_url, data=fs_ancestry_params_json, headers=fs_auth_headers)
    r_ancestry = requests.get('https://sandbox.familysearch.org/platform/tree/ancestry.json', params=fs_ancestry_params, headers=fs_auth_headers)
    r_ancestry_json = r_ancestry.text

    return render(request, 'home/select-person.html', locals())

def map(request):

    return render(request, 'home/map.html', locals())

def timeline(request):

    return render(request, 'home/timeline.html', locals())

def custom_404(request):
    return render(request, 'home/404.html')

def custom_500(request):
    return render(request, 'home/500.html')

