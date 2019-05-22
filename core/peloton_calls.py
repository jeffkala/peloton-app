import json
import sys
import yaml
from getpass import getpass
from pprint import pprint
from core.session import *
from core.session import pelotonAPIManager

def get_credentials(creds_dict=None):
    """Used to look and see if creds are specified if not we will use
       the input() instead.
    """
    try:
        with open('$HOME/creds.key') as f:
            return yaml.safe_load(f)
    except Exception as e:
        pass


def get_connection():
    """ manages the connection to peloton
    """
    creds = get_credentials()
    print(creds)
    if creds:
        user = creds['peloton_user']
        password = creds['peloton_password']
    else:
        user = input('Enter peloton email or username\n')
        password = getpass()
    sess = pelotonAPIManager(user, password)
    sess.login()
    return sess

def me(connection_obj):
    me_url = '/api/me'
    print(me_url)
    me = connection_obj.get(me_url)
    print(type(me.content))
    print(me.content)

    return me.content

def workouts(connection_obj, user):
    wo_url = '/api/user/{}/workouts'.format(user)
    result = connection_obj.get(wo_url)
    return result.json()

def workout_dets(connection_obj, wid):
    wodet_url = '/api/workout/{}'.format(wid)
    result = connection_obj.get(wodet_url)
    return result.json()

def find_workout(connection_obj):
    test_data = {"duration": "5400"}
    fw_url = '/api/v2/ride/archived?browse_category=cycling&content_format=audio,video&limit=100&page=0&duration{}&sort_by=original_air_time&desc=true'.format(test_data['duration'])
    result = connection_obj.get(fw_url)
    return result.json()

def get_artists(connection_obj, workout_id):
    ga_url = '/api/ride/{}/details'.format(workout_id)
    result = connection_obj.get(ga_url)
    return result.json()
