import json
import requests
import settings

FS_CLIENT_ID = settings.FS_CLIENT_ID
FS_AUTH_NETLOC = settings.FS_AUTH_NETLOC

FS_TOKEN_PATH = settings.FS_TOKEN_PATH
FS_TOKEN_PARAMS = settings.FS_TOKEN_PARAMS 

FS_NETLOC = settings.FS_NETLOC

def get_access_token(request):
    if request.session.get('fs_access_token'):
        fs_access_token = request.session.get('fs_access_token')

    else:
        fs_token_url = '%s%s' % (FS_AUTH_NETLOC, FS_TOKEN_PATH)
        fs_auth_code = request.GET.get('code')
        fs_token_params = FS_TOKEN_PARAMS
        fs_token_params['code'] = fs_auth_code
        fs_token_headers = {'content-type': 'application/json'}
        
        r_auth = requests.post(fs_token_url, data=fs_token_params)
        fs_access_token = r_auth.json()['access_token']
        request.session['fs_access_token'] = fs_access_token
    
    return fs_access_token

def get_curr_person_id(request):
    curr_person_id = None
    fs_access_token = get_access_token(request)
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
