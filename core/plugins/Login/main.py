from types import CodeType
import flask
from flask.templating import render_template

name = 'Login/Logout'

requestCPR = None


def cross_plugin_request(args: list):
    if type(args[0]).__name__ == 'str' and args[0] == 'get_path':
        return '/login'
    else:
        return 'denied'


def get_plugins_path_list():
    ret = []
    print(requestCPR())
    for i in requestCPR():
        path = i.cross_plugin_request(['get_path'])
        if type(path).__name__ == 'str' and path == 'denied':
            print('failed with denied')
        else:
            ret.append([path, i.name])
    return ret


def idx_of_login():
    if flask.session.get('userinfo') != None:
        return flask.redirect('/api?action=logout')
    return render_template(
        "plugins_templates/main/index.html",
        plugins_list=get_plugins_path_list(),
        renderText=flask.Markup(render_template(
            'plugins_templates/Login/main.html'))
    )


def idx_of_sign_up():
    return render_template(
        "plugins_templates/main/index.html",
        plugins_list=get_plugins_path_list(),
        renderText=flask.Markup(render_template(
            'plugins_templates/Login/signup.html'))
    )


def register(server: flask.Flask):
    print(requestCPR)
    server.add_url_rule('/login', view_func=idx_of_login,
                        methods=['POST', 'GET'])
    server.add_url_rule('/signup', view_func=idx_of_sign_up,
                        methods=['POST', 'GET'])
    return {
        'registered_api': None
    }
