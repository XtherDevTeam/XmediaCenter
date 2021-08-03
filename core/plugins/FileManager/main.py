from types import CodeType
import flask
from flask.templating import render_template

name = 'FileManager'

requestCPR = None

def cross_plugin_request(args:list):
    if type(args[0]).__name__ == 'str' and args[0] == 'get_path':
        return '/fm'
    else:
        return 'denied' # fuck u

def main():
    return render_template("plugins_templates/fm/main.template")

def register(server:flask.Flask):
    print(requestCPR)
    server.add_url_rule('/fm',view_func=main,methods=['POST','GET'])
    return {
        'registered_api': None
    }