import json,os,sys,pymediainfo,core.api

def init_playlists():
    if os.access('core/storage/playlists.json',os.F_OK):
        None
    else:
        with open('core/storage/playlists.json','w+',encoding='utf-8') as file:
            file.write(json.dumps([]))

def get_playlists():
    init_playlists()
    try:
        with open('core/storage/playlists.json','r+',encoding='utf-8') as file:
            return {'status':'success','playlists':json.loads(file.read())}
    except Exception as e:
        return {'status':'error','reason':str(e)}

def sync_playlists(pls:dict):
    try:
        with open('core/storage/playlists.json','w+',encoding='utf-8') as file:
            file.write(json.dumps(pls['playlists']))
            return {'status':'success'}
    except Exception as e:
        return {'status':'error','reason':str(e)}

def create_playlist(name:str):
    pls = get_playlists()
    if pls['status'] == 'error':
        return pls
    else:
        pls['playlists'].append({ 'name':name,'songs':[] })
        return sync_playlists(pls)

def append_songs(pid:int,path:str):
    try:
        pls = get_playlists()
        if pls['status'] == 'error':
            return pls
        elif len(pls['playlists']) <= pid:
            return {'status':'error','reason':'Out of range'}
        pls['playlists'][pid]['songs'].append(path)
        return sync_playlists(pls)
    except Exception as e:
        return {'status':'error','reason':str(e)}

def get_playlist_id(name:str):
    if name == None:
        return {'status':'error','reason':'Invalid playlist name'}
    else:
        pls = get_playlists()
        if pls['status'] == 'error':
            return pls
        else:
            for i in pls['playlists']:
                if i['name'] == name:
                    return {'status':'success','id':pls['playlists'].index(i)}
    return {'status':'error','reason':'No result'}

def get_songs_info(pid:int):
    pls = get_playlists()
    print(pls['playlists'],len(pls['playlists']))
    if pls['status'] == 'error':
        return pls
    elif len(pls['playlists']) <= pid:
        return {'status':'error','reason':'Out of range'}
    # i -> str
    final = { 'status': 'success','playlist':[] }
    for i in pls['playlists'][pid]['songs']:
        result = pymediainfo.MediaInfo.parse('core/storage/' + core.api.getAbsPath(i))
        final['playlist'].append(
            {
                'title':json.loads(result.to_json())['tracks'][0]['title'],
                'track_name':json.loads(result.to_json())['tracks'][0]['track_name'],
                'album':json.loads(result.to_json())['tracks'][0]['album'],
                'performer':json.loads(result.to_json())['tracks'][0]['performer'],
                'path': core.api.getAbsPath(i)
            }
        )
    return final