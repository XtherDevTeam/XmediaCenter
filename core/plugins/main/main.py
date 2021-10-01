from types import CodeType
import flask
from flask.templating import render_template

import core.xmcp

name = 'main'

requestCPR = None

def cross_plugin_request(args:list):
    return "denied"

def get_plugins_path_list():
    ret = []
    print(requestCPR())
    for i in requestCPR():
        path = i.cross_plugin_request([ 'get_path' ])
        if type(path).__name__ == 'str' and path == 'denied':
            pass
        else:
            ret.append([path,i.name])
    return ret

def main():
    username = ''
    is_logined = False
    if flask.session.get('userinfo') == None:
        is_logined = False
    else:
        is_logined = True
        username = core.xmcp.parseUserInfo(flask.session.get('userinfo'))
    return render_template("plugins_templates/main/index.html",plugins_list=get_plugins_path_list(),renderText=flask.Markup(render_template('plugins_templates/main/main.html',is_logined=is_logined,username=username)))

def register(server:flask.Flask):
    print(requestCPR)
    server.add_url_rule('/main',view_func=main,methods=['POST','GET'])
    return {
        'registered_api': None
    }