from django.shortcuts import redirect
import json
import requests
import settings

FS_CLIENT_ID = settings.FS_CLIENT_ID
FS_AUTH_NETLOC = settings.FS_AUTH_NETLOC

FS_TOKEN_PATH = settings.FS_TOKEN_PATH
FS_TOKEN_PARAMS = settings.FS_TOKEN_PARAMS 

FS_NETLOC = settings.FS_NETLOC

def get_access_token(request):
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
            request.session.set_expiry(1)
            request.session['fs_access_token'] = fs_access_token
            print fs_access_token

    return fs_access_token

def get_curr_person_id(fs_access_token):
    curr_person_id = None
    fs_person_path = '/platform/users/current.json'
    fs_person_url = '%s%s' % (FS_NETLOC, fs_person_path)
    fs_auth_headers = {'Authorization': 'Bearer %s' % fs_access_token}
    r_person = requests.get(fs_person_url, headers=fs_auth_headers)
    r_person_json = r_person.text
    r_person_dict = json.loads(r_person_json)
    curr_person_id = r_person_dict['users'][0]['personId']

    return curr_person_id 

def get_ancestry_data(request):
    curr_person_id = get_curr_person_id(request)
    fs_access_token = get_access_token(request)
    fs_ancestry_path = '/platform/tree/ancestry.json'
    fs_ancestry_url = '%s%s' % (FS_NETLOC, fs_ancestry_path)
    fs_ancestry_params = {'person': curr_person_id}
    fs_ancestry_params_json = json.dumps(fs_ancestry_params)
    fs_auth_headers = {'Authorization': 'Bearer %s' % fs_access_token}
    # r_ancestry = requests.get(fs_ancestry_url, data=fs_ancestry_params_json, headers=fs_auth_headers)
    r_ancestry = requests.get('https://sandbox.familysearch.org/platform/tree/ancestry.json', params=fs_ancestry_params, headers=fs_auth_headers)
    r_ancestry_json = r_ancestry.text

    return r_ancestry_json 
