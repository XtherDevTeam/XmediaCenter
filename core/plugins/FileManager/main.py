from types import CodeType
import flask,core.plugins.FileManager.file_manage,core.api,core.xmcp
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
    #print(requestCPR())
    for i in requestCPR():
        path = i.cross_plugin_request([ 'get_path' ])
        if type(path).__name__ == 'str' and path == 'denied':
            print('failed with denied')
        else:
            ret.append([path,i.name])
    return ret

def get_plugins_names():
    ret = []
    for i in requestCPR():
        ret.append(i.name)
    return ret

def api_request(request:flask.request):
    if type(request.args.get('request')).__name__ == 'str' and request.args.get('request') == 'get_filelist':
        return json.dumps(core.plugins.FileManager.file_manage.get_file_list(request.args.get('path')))
    elif type(request.args.get('request')).__name__ == 'str' and request.args.get('request') == 'download':
        return core.plugins.FileManager.file_manage.response_with_file(request.args.get('path'))
    elif type(request.args.get('request')).__name__ == 'str' and request.args.get('request') == 'is_dir' and flask.session.get('userinfo') != None:
        return core.plugins.FileManager.file_manage.is_directory(request.args.get('path'))
    elif type(request.args.get('request')).__name__ == 'str' and request.args.get('request') == 'remove' and flask.session.get('userinfo') != None:
        return core.plugins.FileManager.file_manage.remove(request.args.get('path'))
    elif type(request.args.get('request')).__name__ == 'str' and request.args.get('request') == 'create_dir' and flask.session.get('userinfo') != None:
        return core.plugins.FileManager.file_manage.create_dir(request.args.get('path'))
    elif type(request.args.get('request')).__name__ == 'str' and request.args.get('request') == 'rename' and flask.session.get('userinfo') != None:
        return core.plugins.FileManager.file_manage.rename(request.args.get('path'),request.args.get('new'))
    elif type(request.args.get('request')).__name__ == 'str' and request.args.get('request') == 'upload' and flask.session.get('userinfo') != None:
        file = request.files.get("file")
        print('request of ' + file.filename)
        file.save('core/storage/' + request.args.get('path') + file.filename)
        return flask.redirect('/fm?path="' + request.args.get('path') + '"')
    else:
        return json.dumps({'status':'error','reason':'Invalid Session'})
    None

def idx_of_fm():
    is_logined = flask.session.get('userinfo') != None
    user = {}
    if is_logined:
        user = core.xmcp.parseUserInfo(flask.session.get('userinfo'))
    try:
        path = core.api.getAbsPath(flask.request.values.get('path'))
        if path == None or path == '/' or core.api.getAbsPath(path) == path or core.api.getAbsPath(path) == '"' + path + '"':
            return render_template("plugins_templates/main/index.html",
                                    plugins_list=get_plugins_path_list(),
                                    renderText=flask.Markup(
                                        render_template(
                                            'plugins_templates/FileManager/main.html',
                                            is_logined = is_logined,
                                            user = user,
                                            path = core.api.getAbsPath(flask.request.values.get('path')),
                                            filenames=core.plugins.FileManager.file_manage.get_file_list(core.api.getAbsPath(flask.request.values.get('path'))),
                                            modules_list=get_plugins_names()
                                        )
                                    ))
        else:
            return flask.redirect('/fm?path=' + core.api.getAbsPath(path))
    except Exception as e:
        return json.dumps({'status':'error','reason':str(e)})
def register(server:flask.Flask):
    #print(requestCPR)
    server.add_url_rule('/fm',view_func=idx_of_fm)
    return {
        'registered_api': ['fm_api']
    }