import json,os,sys,pymediainfo,core.api,hashlib

def init_playlists(userinfo:str):
    # init config directory
    if os.access('core/plugins/MusicPlayer/.musicplayer',os.F_OK):
        None
    else:
        os.mkdir('core/plugins/MusicPlayer/.musicplayer')

    # init user playlists
    if os.access('core/plugins/MusicPlayer/.musicplayer/playlists-' + hashlib.md5(userinfo.encode('utf-8')).hexdigest() + '.json',os.F_OK):
        None
    else:
        with open('core/plugins/MusicPlayer/.musicplayer/playlists-' + hashlib.md5(userinfo.encode('utf-8')).hexdigest() + '.json','w+',encoding='utf-8') as file:
            file.write(json.dumps([]))

def get_playlists(userinfo:str):
    if userinfo == None or userinfo == '':
        return {'status':'error','reason':'Invalid Session'}
    
    init_playlists(userinfo)
    try:
        with open('core/plugins/MusicPlayer/.musicplayer/playlists-' + hashlib.md5(userinfo.encode('utf-8')).hexdigest() + '.json','r+',encoding='utf-8') as file:
            return {'status':'success','playlists':json.loads(file.read())}
    except Exception as e:
        return {'status':'error','reason':str(e)}

def sync_playlists(pls:dict,userinfo:str):
    try:
        if userinfo == None or userinfo == '':
            None
        with open('core/plugins/MusicPlayer/.musicplayer/playlists-' + hashlib.md5(userinfo.encode('utf-8')).hexdigest() + '.json','w+',encoding='utf-8') as file:
            file.write(json.dumps(pls['playlists']))
            return {'status':'success'}
    except Exception as e:
        return {'status':'error','reason':str(e)}

def create_playlist(name:str,userinfo:str):
    pls = get_playlists(userinfo)
    if pls['status'] == 'error':
        return pls
    else:
        pls['playlists'].append({ 'name':name,'songs':[] })
        return sync_playlists(pls,userinfo)

def append_songs(pid:int,path:str,userinfo:str):
    try:
        print('path:',path)
        if path != None and path[0] == '"':
            path = path[1:-1]
        pls = get_playlists(userinfo)
        if pls['status'] == 'error':
            return pls
        elif len(pls['playlists']) <= pid:
            return {'status':'error','reason':'Out of range'}
        elif pls['playlists'][pid]['songs'].count(path):
            return {'status':'success'}
        pls['playlists'][pid]['songs'].append(path)
        return sync_playlists(pls,userinfo)
    except Exception as e:
        return {'status':'error','reason':str(e)}

def remove_song(pid:int,path:str,userinfo:str):
    try:
        pls = get_playlists(userinfo)
        if pls['status'] == 'error':
            return pls
        if pls['playlists'][pid]['songs'].count(path) == 0:
            print(pls['playlists'][pid]['songs'])
            return {'status':'error','reason':'song is not in list:' + path}
        del pls['playlists'][pid]['songs'][pls['playlists'][pid]['songs'].index(path)]
        return sync_playlists(pls,userinfo)
    except Exception as e:
        return {'status':'error','reason':str(e)}

def remove_playlist(pid:int,userinfo:str):
    try:
        pls = get_playlists(userinfo)
        if pls['status'] == 'error':
            return pls
        del pls['playlists'][pid]
        return sync_playlists(pls,userinfo)
    except Exception as e:
        return {'status':'error','reason':str(e)}

def get_playlist_id(name:str,userinfo:str):
    if name == None:
        return {'status':'error','reason':'Invalid playlist name'}
    else:
        pls = get_playlists(userinfo)
        if pls['status'] == 'error':
            return pls
        else:
            for i in pls['playlists']:
                if i['name'] == name:
                    return {'status':'success','id':pls['playlists'].index(i)}
    return {'status':'error','reason':'No result'}

def get_songs_info(pid:int,userinfo:str):
    pls = get_playlists(userinfo)
    print(pls['playlists'],len(pls['playlists']))
    if pls['status'] == 'error':
        return pls
    elif len(pls['playlists']) <= pid:
        return {'status':'error','reason':'Out of range'}
    # i -> str
    final = { 'status': 'success','playlist':[] }
    for i in pls['playlists'][pid]['songs']:
        result = pymediainfo.MediaInfo.parse('core/storage/' + core.api.getAbsPath(i))
        try:
            final['playlist'].append(
                {
                    'title':json.loads(result.to_json())['tracks'][0]['title'],
                    'track_name':json.loads(result.to_json())['tracks'][0].get('track_name'),
                    'album':json.loads(result.to_json())['tracks'][0].get('album'),
                    'performer':json.loads(result.to_json())['tracks'][0].get('performer'),
                    'path': core.api.getAbsPath(i)
                }
            )
        except Exception as e:
            print('failed: ' + core.api.getAbsPath(i))
    return final