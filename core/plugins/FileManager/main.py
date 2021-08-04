from types import CodeType
import flask,core.plugins.FileManager.file_manage
from flask.globals import g
from flask.templating import render_template
import json

name = 'FileManager'

requestCPR = None

def cross_plugin_request(args:list):
    if type(args[0]).__name__ == 'str' and args[0] == 'get_path':
        return '/fm'
    else:
        return 'denied'

def get_plugins_path_list():
    ret = []
    print(requestCPR())
    for i in requestCPR():
        if i.name == name:
            continue
        path = i.cross_plugin_request([ 'get_path' ])
        if type(path).__name__ == 'str' and path == 'denied':
            print('failed with denied')
        else:
            ret.append([path,i.name])
    return ret

def api_request(request:flask.request):
    if type(request.args.get('request')).__name__ == 'str' and request.args.get('request') == 'get_filelist':
        return json.dumps(core.plugins.FileManager.file_manage.get_file_list(request.args.get('path')))
    elif type(request.args.get('request')).__name__ == 'str' and request.args.get('request') == 'download':
        return core.plugins.FileManager.file_manage.response_with_file(request.args.get('path'))
    None

def idx_of_fm():
    return render_template("plugins_templates/main/index.html",plugins_list=get_plugins_path_list(),renderText=flask.Markup(render_template('plugins_templates/FileManager/main.html')))

def register(server:flask.Flask):
    print(requestCPR)
    server.add_url_rule('/fm',view_func=idx_of_fm)
    return {
        'registered_api': ['fm_api']
    }