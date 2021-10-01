from os import F_OK
import os
from types import CodeType
import flask,core.plugins.FileManager.file_manage,core.api,core.xmcp,core.plugins.video_player.video_apis
from flask.globals import g
from flask.templating import render_template
import json

name = 'Video Player'

requestCPR = None

def cross_plugin_request(args:list):
    if type(args[0]).__name__ == 'str' and args[0] == 'get_path':
        return '/video'
    else:
        return 'denied'

def get_plugins_path_list():
    ret = []
    #print(requestCPR())
    for i in requestCPR():
        path = i.cross_plugin_request([ 'get_path' ])
        if type(path).__name__ == 'str' and path == 'denied':
            pass
        else:
            ret.append([path,i.name])
    return ret

def api_request(request:flask.request):
    request_item = request.values.get('request')
    if request_item == 'damuku':
        video_path = request.values.get('request_video')
        # fetch from bilibili
        if video_path.endswith('v3/?id=undefined'):
            video_path = video_path[0:0-len('v3/?id=undefined')]
        ret = {'code':0,'data':[]}
        print('trying access:',('core/storage/' + core.api.getAbsPath(video_path))[0:-4] + '.cmt.xml')
        with open(file='core/storage/' + core.api.getAbsPath(video_path)[0:-4] + '.cmt.xml',mode='r') as f:
            ret['data'] = core.plugins.video_player.video_apis.damuku_parser(f.read().encode(encoding='utf-8'))
        
        response = flask.make_response(json.dumps(ret))
        response.headers['Content-Type']= 'application/json'
        return response
    None
                

def idx_of_vp():
    is_logined = flask.session.get('userinfo') != None
    user = {}
    if is_logined:
        user = core.xmcp.parseUserInfo(flask.session.get('userinfo'))
    return render_template("plugins_templates/main/index.html",
                            plugins_list=get_plugins_path_list(),
                            renderText=flask.Markup(
                                render_template(
                                    'plugins_templates/video_player/main.html',
                                    is_logined = is_logined,
                                    user = user,
                                    path = core.api.getAbsPath(flask.request.values.get('path')),
                                    filename = core.api.get_filename(flask.request.values.get('path'))
                                )
                            ))

def register(server:flask.Flask):
    #print(requestCPR)
    server.add_url_rule('/video',view_func=idx_of_vp)
    return {
        'registered_api': ['vp_api']
    }