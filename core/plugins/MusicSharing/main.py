from types import CodeType
import flask,core.plugins.FileManager.file_manage,core.api,core.xmcp
from flask.globals import g
from flask.templating import render_template
import json
import pymediainfo
from mutagen import File

name = 'Mini music player'

requestCPR = None

def cross_plugin_request(args:list):
    return 'denied'

def get_plugins_path_list():
    ret = []
    #print(requestCPR())
    for i in requestCPR():
        if i.name == name:
            continue
        path = i.cross_plugin_request([ 'get_path' ])
        if type(path).__name__ == 'str' and path == 'denied':
            pass
        else:
            ret.append([path,i.name])
    return ret

def api_request(request:flask.request):
    try:
        file = File('core/storage/' + core.api.getAbsPath(core.api.getAbsPath(request.values.get('path'))))
    except Exception as e:
        return {'status':'error', 'reason': str(e)}
    return flask.Response(file['APIC:'].data,mimetype='image/jpeg')
    

def idx_of_mmp():
    is_logined = flask.session.get('userinfo') != None
    user = {}
    if is_logined:
        user = core.xmcp.parseUserInfo(flask.session.get('userinfo'))
    if core.api.getAbsPath(flask.request.values.get('path')) == None:
        return {'status':'error', 'reason': 'invalid music path'}
    result = None
    try:
        result = pymediainfo.MediaInfo.parse('core/storage/' + core.api.getAbsPath(core.api.getAbsPath(flask.request.values.get('path'))))
    except Exception as e:
        return {'status':'error', 'reason': str(e)}
    try:
        result = {
                'title':json.loads(result.to_json())['tracks'][0]['title'],
                'track_name':json.loads(result.to_json())['tracks'][0].get('track_name'),
                'album':json.loads(result.to_json())['tracks'][0].get('album'),
                'performer':json.loads(result.to_json())['tracks'][0].get('performer'),
                'path': core.api.getAbsPath(core.api.getAbsPath(flask.request.values.get('path')))
            }
    except Exception as e:
        print('failed: ' + core.api.getAbsPath(core.api.getAbsPath(flask.request.values.get('path'))))
    return flask.Markup(
                        render_template(
                            'plugins_templates/MusicSharing/main.html',
                            is_logined = is_logined,
                            user = user,
                            song_info = result,

                        )
                    )

def register(server:flask.Flask):
    #print(requestCPR)
    server.add_url_rule('/mmp',view_func=idx_of_mmp)
    return {
        'registered_api': ['mmp_album_image']
    }