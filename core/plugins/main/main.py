from types import CodeType
import flask
from flask.templating import render_template

name = 'main'

requestCPR = None

def cross_plugin_request(args:list):
    return "denied"

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

def main():
    return render_template("plugins_templates/main/index.html",plugins_list=get_plugins_path_list(),renderText=flask.Markup(render_template('plugins_templates/main/main.html')))

def register(server:flask.Flask):
    print(requestCPR)
    server.add_url_rule('/main',view_func=main,methods=['POST','GET'])
    return {
        'registered_api': None
    }