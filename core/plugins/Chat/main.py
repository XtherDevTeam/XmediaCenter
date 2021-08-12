from werkzeug.datastructures import CharsetAccept
from core.plugins.Chat.apis import get_info_file, init_info_file
from types import CodeType
import flask
import core.plugins.FileManager.file_manage
import core.api
import core.xmcp
from flask.globals import g
from flask.templating import render_template
import json
import importlib

name = 'Chat'

requestCPR = None

chatroom_api = importlib.import_module('core.plugins.Chat.apis')


def cross_plugin_request(args: list):
    if type(args[0]).__name__ == 'str' and args[0] == 'get_path':
        return '/chat'
    else:
        return 'denied'


def get_plugins_path_list():
    ret = []
    # print(requestCPR())
    for i in requestCPR():
        if i.name == name:
            continue
        path = i.cross_plugin_request(['get_path'])
        if type(path).__name__ == 'str' and path == 'denied':
            print('failed with denied')
        else:
            ret.append([path, i.name])
    return ret


def idx_of_chat():
    is_logined = flask.session.get('userinfo') != None
    user = {}
    if is_logined:
        user = core.xmcp.parseUserInfo(flask.session.get('userinfo'))
    return render_template("plugins_templates/main/index.html",
                           plugins_list=get_plugins_path_list(),
                           renderText=flask.Markup(
                               render_template(
                                   'plugins_templates/Chat/main.html',
                                   is_logined=is_logined,
                                   user=user,
                                   joined=chatroom_api.get_joined_groups(user.get('u'))
                               )
                           ))


def idx_of_chatroom(cid):
    is_logined = flask.session.get('userinfo') != None
    user = {}
    if is_logined:
        user = core.xmcp.parseUserInfo(flask.session.get('userinfo'))
    return render_template("plugins_templates/main/index.html",
                           plugins_list=get_plugins_path_list(),
                           renderText=flask.Markup(
                               render_template(
                                   'plugins_templates/Chat/chatroom.html',
                                   is_logined=is_logined,
                                   user=user,
                               )
                           ))


def api_request(request: flask.request):
    request_item = request.values.get('request')
    chatroom_api.init_info_file()
    if flask.session.get('userinfo') == None:
        return {'status': 'error', 'reason': 'Invalid Session'}
    if request_item == None:
        return {'status': 'error', 'reason': 'Invalid request'}
    elif request_item == 'create_chatroom':
        name = request.values.get('name')
        if name == None:
            return {'status': 'error', 'reason': 'Invalid request'}
        file = chatroom_api.get_info_file()

        if core.xmcp.parseUserInfo(flask.session.get('userinfo'))['u'] not in file['users']:
            file['users'][core.xmcp.parseUserInfo(
                flask.session.get('userinfo'))['u']] = []

        file['groups'].append(name)
        file['users'][core.xmcp.parseUserInfo(flask.session.get('userinfo'))[
            'u']].append(name)
        chatroom_api.sync_info_file(file)
        return {'status': 'success'}
    elif request_item == 'remove_chatroom':
        name = request.values.get('name')
        if name == None:
            return {'status': 'error', 'reason': 'Invalid request'}
        file = chatroom_api.get_info_file()

        if core.xmcp.parseUserInfo(flask.session.get('userinfo'))['u'] not in file['users']:
            file['users'][core.xmcp.parseUserInfo(
                flask.session.get('userinfo'))['u']] = []

        if file['users'][core.xmcp.parseUserInfo(flask.session.get('userinfo'))['u']].count(name) == 0:
            return {'status': 'error', 'reason': 'No premission to do this'}
        del file['users'][core.xmcp.parseUserInfo(flask.session.get('userinfo'))[
            'u']][file['users'][core.xmcp.parseUserInfo(flask.session.get('userinfo'))['u']].index(name)]
        del file['groups'][file['groups'].index(name)]

        chatroom_api.sync_info_file(file)
        return {'status': 'success'}
    elif request_item == 'join_chatroom':
        name = request.values.get('name')
        if name == None:
            return {'status': 'error', 'reason': 'Invalid request'}
        file = chatroom_api.get_info_file()

        if core.xmcp.parseUserInfo(flask.session.get('userinfo'))['u'] not in file['users']:
            file['users'][core.xmcp.parseUserInfo(
                flask.session.get('userinfo'))['u']] = []

        if file['groups'].count(name) == 0:
            return {'status': 'error', 'reason': 'Not exist'}

        file['users'][core.xmcp.parseUserInfo(flask.session.get('userinfo'))[
            'u']].append(name)
        chatroom_api.sync_info_file(file)
        return {'status': 'success'}
    elif request_item == 'exit_chatroom':
        name = request.values.get('name')
        if name == None:
            return {'status': 'error', 'reason': 'Invalid request'}
        file = chatroom_api.get_info_file()

        if core.xmcp.parseUserInfo(flask.session.get('userinfo'))['u'] not in file['users']:
            file['users'][core.xmcp.parseUserInfo(
                flask.session.get('userinfo'))['u']] = []

        if file['users'][core.xmcp.parseUserInfo(flask.session.get('userinfo'))['u']].count(name) == 0:
            return {'status': 'error', 'reason': 'Not exist'}

        del file['users'][core.xmcp.parseUserInfo(flask.session.get('userinfo'))[
            'u']][file['users'][core.xmcp.parseUserInfo(flask.session.get('userinfo'))['u']].index(name)]
        chatroom_api.sync_info_file(file)
        return {'status': 'success'}
    else:
        return {'status': 'error', 'reason': 'Invalid request'}

def register(server: flask.Flask):
    # print(requestCPR)
    print('registered')
    server.add_url_rule('/chat', view_func=idx_of_chat)
    server.add_url_rule('/chatroom/<cid>', view_func=idx_of_chatroom)
    return {
        'registered_api': ['chat_api']
    }
