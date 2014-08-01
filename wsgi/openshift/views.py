from django.shortcuts import render, redirect
import json
import os
import requests
import service
import settings
import urllib

FS_AUTH_NETLOC = settings.FS_AUTH_NETLOC
FS_AUTH_PATH = settings.FS_AUTH_PATH
FS_AUTH_PARAMS = settings.FS_AUTH_PARAMS 

def home(request):

    return render(request, 'home/home.html', locals())

def select_person_old(request):
    print '--------------'
    fs_token_url = '%s%s' % (FS_AUTH_NETLOC, FS_TOKEN_PATH)
    fs_auth_code = request.GET.get('code')
    # -----
    # Delete this next line once the redirect uri is working
    # fs_auth_code = '-80-42-1041102-84-98675-623-9080124705073-11268-111-1219742100861276495712712281'
    # -----
    fs_token_params = FS_TOKEN_PARAMS
    fs_token_params['code'] = fs_auth_code
    fs_token_params_json = json.dumps(fs_token_params)
    fs_token_headers = {'content-type': 'application/json'}
    
    r_auth = requests.post(fs_token_url, data=fs_token_params_json, headers=fs_token_headers)
    print '(((((((((((('
    print r_auth
    print r_auth.json()
    fs_access_token = r_auth.json()['access_token']

    # -----
    # Delete this next line once the redirect uri is working
    # fs_access_token = 'USYSC4220735F08DD315C29BB00E59ACFF6A_idses-int02.a.fsglobal.net'
    # -----
    print '============='
    # -------------------------------------------------------------------------
    # Get ancestry data
    fs_ancestry_path = '/platform/tree/ancestry.json'
    fs_ancestry_url = '%s%s' % (FS_NETLOC, fs_ancestry_path)
    fs_ancestry_params = {'person': 'KW71-SFK'}
    fs_ancestry_params_json = json.dumps(fs_ancestry_params)
    fs_auth_headers = {'Authorization': 'Bearer %s' % fs_access_token}
    # r_ancestry = requests.get(fs_ancestry_url, data=fs_ancestry_params_json, headers=fs_auth_headers)
    r_ancestry = requests.get('https://sandbox.familysearch.org/platform/tree/ancestry.json', params=fs_ancestry_params, headers=fs_auth_headers)
    r_ancestry_json = r_ancestry.text

    return render(request, 'home/select-person-old.html', locals())

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

def test(request):
    return render(request, 'home/test.html', locals())

def test3(request):
    return render(request, 'home/test3.html', locals())

def select_person(request):
    response = render(request, 'home/select-person-simp.html', locals())
    fs_access_token = request.COOKIES.get('fs_access_token')
    print fs_access_token
    if fs_access_token == None:
        print 'hi'
        auth_code = request.GET.get('code')

        token_response = requests.post('https://sandbox.familysearch.org/cis-web/oauth2/v3/token', {'grant_type': 'authorization_code', 'code': auth_code, 'client_id': 'WCQY-7J1Q-GKVV-7DNM-SQ5M-9Q5H-JX3H-CMJK'}).json()
        fs_access_token = token_response.get('access_token')
        if not fs_access_token:
            return redirect('/test3')
        else:
            response.set_cookie('fs_access_token', fs_access_token, max_age=3540)
    print fs_access_token
    person_response = requests.get('https://sandbox.familysearch.org/platform/tree/persons/KW71-481', headers={'Accept': 'application/x-gedcomx-v1+json', 'Authorization': 'Bearer ' + fs_access_token}).json()
    print person_response

    # next steps: allow logout (by deleting cookie) and redirect
    # also delete access token https://familysearch.org/developers/docs/api/authentication/Delete_Access_Token_usecase
    return response

