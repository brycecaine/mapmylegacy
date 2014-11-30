from openshift import settings
from PIL import Image
import json
import logging
import os
import requests
import shutil

FS_CLIENT_ID = settings.FS_CLIENT_ID
FS_AUTH_NETLOC = settings.FS_AUTH_NETLOC

FS_TOKEN_PATH = settings.FS_TOKEN_PATH
FS_TOKEN_PARAMS = settings.FS_TOKEN_PARAMS 

FS_NETLOC = settings.FS_NETLOC
FS_PERSON_PATH = settings.FS_PERSON_PATH 

IMG_SIZE = 96, 96

def get_access_token(request):
    # Get access token if it exists in the session variables
    fs_access_token = request.session.get('fs_access_token')

    # If the access token doesn't exist, have user authenticate against familysearch for it
    if fs_access_token == None:
        # Get authorization code from url
        auth_code = request.GET.get('code')

        # Get access token
        get_acc_tok_url = '%s%s' % (FS_AUTH_NETLOC, FS_TOKEN_PATH)
        get_acc_tok_data = {'grant_type': 'authorization_code',
                            'code': auth_code,
                            'client_id': FS_CLIENT_ID}
        token_response = requests.post(get_acc_tok_url, get_acc_tok_data).json()
        fs_access_token = token_response.get('access_token')

        # If response contains access token, add the access token to a session
        # variable
        if fs_access_token:
            request.session.set_expiry(1800)
            request.session['fs_access_token'] = fs_access_token

            fs_name = get_curr_person_data(fs_access_token, 'name')
            request.session['fs_name'] = fs_name

    return fs_access_token

def del_access_token(request):
    status = False
    fs_access_token = request.session.get('fs_access_token')

    # Delete access token
    del_acc_tok_url = '%s%s?access_token=%s' % (FS_AUTH_NETLOC, FS_TOKEN_PATH, fs_access_token)
    del_resp = requests.delete(del_acc_tok_url)

    # Delete fs_access_token session variable
    request.session.flush()

    status = True

    return status

def get_curr_person_data(fs_access_token, kind='all'):
    curr_person_id = None
    fs_person_path = '/platform/users/current.json'
    fs_person_url = '%s%s' % (FS_NETLOC, fs_person_path)
    fs_auth_headers = {'Authorization': 'Bearer %s' % fs_access_token}
    r_person = requests.get(fs_person_url, headers=fs_auth_headers)
    r_person_json = r_person.text

    try:
        r_person_dict = json.loads(r_person_json)

        return_val = r_person_dict

        if kind == 'id':
            return_val = r_person_dict['users'][0]['personId']

        elif kind == 'name':
            return_val = r_person_dict['users'][0]['displayName']

    except ValueError:
        return_val = None

    return return_val    

def get_person_data(fs_access_token, person_id):
    # get_person_url = '%s%s%s' % (FS_AUTH_NETLOC, FS_PERSON_PATH, person_id)
    get_person_url = '%s%s%s/notes' % (FS_AUTH_NETLOC, FS_PERSON_PATH, person_id)
    get_person_headers = {'Accept': 'application/x-gedcomx-v1+json',
                          'Authorization': 'Bearer ' + fs_access_token}
    person_response = requests.get(get_person_url, headers=get_person_headers).text
    person_data = json.loads(person_response)

    # Still need to pick the correct note among several notes
    person_data = person_data['persons'][0]['notes'][0]['text']
    event_list = person_data.split('\n')
    for event in event_list:
        items = event.split(' - ')
    print '========================'
    print json.dumps(person_data, indent=4)

    return person_data

def get_ancestry_data(fs_access_token, person_id):
    fs_ancestry_path = '/platform/tree/ancestry.json'
    fs_ancestry_url = '%s%s' % (FS_NETLOC, fs_ancestry_path)
    fs_ancestry_params = {'person': person_id}
    fs_ancestry_params_json = json.dumps(fs_ancestry_params)
    fs_auth_headers = {'Authorization': 'Bearer %s' % fs_access_token}
    # r_ancestry = requests.get(fs_ancestry_url, data=fs_ancestry_params_json, headers=fs_auth_headers)
    r_ancestry = requests.get('https://sandbox.familysearch.org/platform/tree/ancestry.json', params=fs_ancestry_params, headers=fs_auth_headers)
    ancestry_json = r_ancestry.text

    return ancestry_json 

def get_ancestry_photos(fs_access_token, person_id):
    fs_auth_headers = {'Authorization': 'Bearer %s' % fs_access_token}

    # Get ancestry data
    ancestry_json = get_ancestry_data(fs_access_token, person_id)
    ancestry = json.loads(ancestry_json)
    ancestor_list = []

    for ancestor in ancestry['persons']:
        person_id = ancestor['id']
        filename = '%s.jpg' % person_id
        name = ancestor['display']['name']
        relation = ancestor['display']['ascendancyNumber']
        ancestor_list.append({'person_id': person_id,
                              'filename': filename,
                              'name': name,
                              'relation': relation})

    portraits_json = json.dumps(ancestor_list)
    
    # Retrieve portrait photos and save them to the static directory for use in
    # the game
    for ancestor in ancestor_list:
        fs_portrait_path = '/platform/tree/persons/%s/portrait' % ancestor['person_id']
        fs_portrait_url = '%s%s' % (FS_NETLOC, fs_portrait_path)
        fs_params = {'default': 'http://cdn.flaticon.com/png/256/36601.png'}
        r_portrait = requests.get(fs_portrait_url, params=fs_params, headers=fs_auth_headers, stream=True)
        portrait_path = 'static/img/%s' % ancestor['filename']

        if r_portrait.status_code == 200:
            with open(portrait_path, 'wb') as f:
                r_portrait.raw.decode_content = True
                shutil.copyfileobj(r_portrait.raw, f)       

    ped_filenames = [ped_filename['filename'] for ped_filename in ancestor_list]
    for filename in os.listdir('/home/action/workspace/mapmylegacy/wsgi/openshift/static/img'):
        if filename in ped_filenames:
            print 1
            outfile = '/home/action/workspace/mapmylegacy/wsgi/openshift/static/img/%s' % filename
            print 2
            try:
                print 3
                im = Image.open('/home/action/workspace/mapmylegacy/wsgi/openshift/static/img/%s' % filename)
                print 4
                im.thumbnail(IMG_SIZE, Image.ANTIALIAS)
                print 5
                im.save(outfile, 'JPEG')
                print 6
            except IOError:
                print "Cannot create thumbnail for '%s'" % filename
                shutil.copy('/home/action/workspace/mapmylegacy/wsgi/openshift/static/img/placeholder.jpg', '/home/action/workspace/mapmylegacy/wsgi/openshift/static/img/%s' % filename)

    return portraits_json
