from types import CodeType
import flask
from flask.templating import render_template

name = 'Login'

requestCPR = None

def cross_plugin_request(args:list):
    if type(args[0]).__name__ == 'str' and args[0] == 'get_path':
        return '/login'
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

def idx_of_login():
    return render_template("plugins_templates/main/index.html",plugins_list=get_plugins_path_list(),renderText=flask.Markup(render_template('plugins_templates/Login/main.html')))
 
def register(server:flask.Flask):
    print(requestCPR)
    server.add_url_rule('/login',view_func=idx_of_login,methods=['POST','GET'])
    return {
        'registered_api': None
    }