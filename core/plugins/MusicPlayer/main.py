from types import CodeType
import flask,core.plugins.MusicPlayer.music_apis,core.api,core.xmcp,core.plugins.MusicPlayer.counter,pymediainfo
from werkzeug.utils import redirect
from flask.globals import g
from flask.templating import render_template
import json

name = 'MusicPlayer'

requestCPR = None

def cross_plugin_request(args:list):
    if type(args[0]).__name__ == 'str' and args[0] == 'get_path':
        return '/music'
    else:
        return 'denied'

def get_plugins_path_list():
    ret = []
    #print(requestCPR())
    for i in requestCPR():
        path = i.cross_plugin_request([ 'get_path' ])
        if type(path).__name__ == 'str' and path == 'denied':
            print('failed with denied')
        else:
            ret.append([path,i.name])
    return ret

def api_request(request:flask.request):
    request_item = request.values.get('request')
    if request_item == None:
        return json.dumps({'status':'error','reason':'unknown request'})
    if request_item == 'get_playlist_id':
        pname = request.values.get('name')
        if pname == None:
            return json.dumps({'status':'error','reason':'unknown request'})
        if pname[0] == '"':
            pname = pname[1:-1]
        return json.dumps(core.plugins.MusicPlayer.music_apis.get_playlist_id(pname,flask.session.get('userinfo')))
    elif request_item == 'get_playlists':
        return json.dumps(core.plugins.MusicPlayer.music_apis.get_playlists(flask.session.get('userinfo')))
    elif request_item == 'create_playlist':
        pname = request.values.get('name')
        if pname == None:
            return json.dumps({'status':'error','reason':'unknown request'})
        if pname[0] == '"':
            pname = pname[1:-1]
        return json.dumps(core.plugins.MusicPlayer.music_apis.create_playlist(pname,flask.session.get('userinfo')))
    elif request_item == 'half_pasted_detect':
        filepath = request.values.get('path')
        if filepath == None or filepath == '':
            return json.dumps({'status':'error','reason':'unknown request'})
        elif flask.session.get('userinfo') == None:
            return json.dumps({'status':'error','reason':'Invalid Session'})
        try:
            audio_info = pymediainfo.MediaInfo.parse('core/storage/' + core.api.getAbsPath(filepath))
            return core.plugins.MusicPlayer.counter.update_counter_file(flask.session.get('userinfo'),json.loads(audio_info.to_json())['tracks'][0]['title'])
        except Exception as e:
            return {'status':'error','reason':str(e)}
    elif request_item == 'add_song':
        pid = request.values.get('pid')
        path = request.values.get('path') # already is abs path
        if pid == None or path == None:
            return json.dumps({'status':'error','reason':'unknown request'})
        pid = int(pid)
        path = core.api.getAbsPath(path)
        return json.dumps(core.plugins.MusicPlayer.music_apis.append_songs(pid,path,flask.session.get('userinfo')))
    elif request_item == 'remove_song':
        pid = request.values.get('pid')
        path = request.values.get('path') # already is abs path
        if pid == None or path == None:
            return json.dumps({'status':'error','reason':'unknown request'})
        pid = int(pid)
        return json.dumps(core.plugins.MusicPlayer.music_apis.remove_song(pid,path,flask.session.get('userinfo')))
    elif request_item == 'remove_playlist':
        pid = request.values.get('pid')
        if pid == None:
            return json.dumps({'status':'error','reason':'unknown request'})
        pid = int(pid)
        return json.dumps(core.plugins.MusicPlayer.music_apis.remove_playlist(pid,flask.session.get('userinfo')))
    

def idx_of_music():
    is_logined = flask.session.get('userinfo') != None
    user = {}
    if is_logined:
        user = core.xmcp.parseUserInfo(flask.session.get('userinfo'))
    return render_template("plugins_templates/main/index.html",
                            plugins_list=get_plugins_path_list(),
                            renderText=flask.Markup(
                                render_template(
                                    'plugins_templates/MusicPlayer/main.html',
                                    is_logined = is_logined,
                                    user = user,
                                    playlists = core.plugins.MusicPlayer.music_apis.get_playlists(flask.session.get('userinfo'))
                                )
                            ))

def idx_of_playlists(name:str):
    is_logined = flask.session.get('userinfo') != None
    user = {}
    if is_logined:
        user = core.xmcp.parseUserInfo(flask.session.get('userinfo'))
    return render_template("plugins_templates/main/index.html",
                            plugins_list=get_plugins_path_list(),
                            renderText=flask.Markup(
                                render_template(
                                    'plugins_templates/MusicPlayer/playlists.html',
                                    is_logined = is_logined,
                                    user = user,
                                    playlists = core.plugins.MusicPlayer.music_apis.get_playlists(flask.session.get('userinfo')),
                                    pid = core.plugins.MusicPlayer.music_apis.get_playlist_id(name,flask.session.get('userinfo'))['id'],
                                    info = core.plugins.MusicPlayer.music_apis.get_songs_info(core.plugins.MusicPlayer.music_apis.get_playlist_id(name,flask.session.get('userinfo'))['id'],flask.session.get('userinfo')),
                                    name = name
                                )
                            ))

def idx_of_count():
    is_logined = flask.session.get('userinfo') != None
    user = {}
    if is_logined:
        user = core.xmcp.parseUserInfo(flask.session.get('userinfo'))
    return render_template("plugins_templates/main/index.html",
                            plugins_list=get_plugins_path_list(),
                            renderText=flask.Markup(
                                render_template(
                                    'plugins_templates/MusicPlayer/counter.html',
                                    is_logined = is_logined,
                                    user = user,
                                    song_count = core.plugins.MusicPlayer.counter.get_program_readable_counter_data(flask.session.get('userinfo'))
                                )
                            ))

def register(server:flask.Flask):
    #print(requestCPR)
    server.add_url_rule('/music',view_func=idx_of_music)
    server.add_url_rule('/music/count',view_func=idx_of_count)
    server.add_url_rule('/music/playlists/<name>',view_func=idx_of_playlists)
    return {
        'registered_api': ['music_api']
    }