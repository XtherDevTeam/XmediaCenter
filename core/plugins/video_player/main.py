from os import F_OK
import os
from types import CodeType
import flask,core.plugins.FileManager.file_manage,core.api,core.xmcp
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
            print('failed with denied')
        else:
            ret.append([path,i.name])
    return ret

def api_request(request:flask.request):
    request_item = request.values.get('request')
    if request_item == 'damuku':
        video_path = str(request.values.get('path'))
        # fetch from bilibili
        if video_path.endswith('.flv'): 
            print('trying access:',('core/storage/' + core.api.getAbsPath(video_path))[0:-4] + '.cmt.xml')
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
                                )
                            ))

def register(server:flask.Flask):
    #print(requestCPR)
    server.add_url_rule('/video',view_func=idx_of_vp)
    return {
        'registered_api': ['vp_api']
    }