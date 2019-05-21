from core.session import pelotonAPIManager
from core.peloton_calls import *
from getpass import getpass

def main():
    u = input('Enter peloton email or username\n')
    p = getpass()
    sess = pelotonAPIManager(u,p)
    print(u,p)
    print(sess.login())
    #my_dets = me(sess)
    #pprint(my_dets)
    #wo = workouts(uid)
    #pprint(wo.keys())
    #pprint(wo['count'])
    #pprint(wo['summary'])
    #data = wo['data']
    #for x in data:
    #    print(x['id'])
    #det = workout_dets(sess, '7c4a0f193c8c478f88bda3f5cc803fc9')
    #print(det)
    test = find_workout(sess)
    for x in test['data']:
        pprint(x['id'])
        artist = get_artists(sess, str(x['id']))
        #pprint(artist)
        for x in artist['playlist']['songs']:
            if 'Bon Jovi' in str(x['artists'][0]['artist_name']):
                print('A ride has a favorite artist {}:{}'.format(x['artists'][0]['artist_name'], x['title']))
            #print(x['artists'][0]['artist_name'], x['title'])
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)

