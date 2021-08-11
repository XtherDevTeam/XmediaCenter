from types import CodeType
import flask,core.plugins.FileManager.file_manage,core.api,core.xmcp
from flask.globals import g
from flask.templating import render_template
import json

name = 'Server Manage'

requestCPR = None

def cross_plugin_request(args:list):
    if type(args[0]).__name__ == 'str' and args[0] == 'get_path':
        return '/admin'
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
    None

def idx_of_admin():
    is_logined = flask.session.get('userinfo') != None
    user = {}
    if is_logined:
        user = core.xmcp.parseUserInfo(flask.session.get('userinfo'))

    pool = core.api.get_register_requests_pool()
    pool_msg = []
    if pool['status'] != 'error':
        for i in pool['file']['requests']:
            pool_msg.append(core.xmcp.parseUserInfo(i))
    return render_template("plugins_templates/main/index.html",
                            plugins_list=get_plugins_path_list(),
                            renderText=flask.Markup(
                                render_template(
                                    'plugins_templates/Admin/main.html',
                                    is_logined = is_logined,
                                    user = user,
                                    filenames=core.plugins.FileManager.file_manage.get_file_list(core.api.getAbsPath(flask.request.values.get('path'))),
                                    regreqpool = pool,
                                    poolinfo = pool_msg
                                )
                            ))

def register(server:flask.Flask):
    #print(requestCPR)
    server.add_url_rule('/admin',view_func=idx_of_admin)
    return {
        'registered_api': None
    }