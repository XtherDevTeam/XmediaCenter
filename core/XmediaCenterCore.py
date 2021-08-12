# Main core

import os,json,sys,flask,core.api,core.xmcp,hashlib,importlib
from flask.wrappers import Request
from flask.templating import render_template

with open('config.json','r+') as config:
    config = json.loads(config.read())

log_file = open('server.log','w+')

def printLog(toprint:str,level:str):
    final = ''
    if level == "i":
        final = '[XmediaCenter/INFO] ' + toprint + '\n'
    elif level == 'e':
        final = '[XmediaCenter/ERROR] ' + toprint + '\n'
    elif level == 'w':
        final = '[XmediaCenter/WARN] ' + toprint + '\n'
    else:
        final = '[XmediaCenter/BadLevel] ' + toprint + '\n'
    log_file.write(final)
    print(final,end='')


status = "stopped"
if os.access(core.api.getAbsPath('core/info.json'),os.F_OK) == False:
    # first run
    printLog(".exmc path does not exist. will create one",'i')
    with open(core.api.getAbsPath('core/info.json'),'w+') as file:
        # default config file template
        dict = {
            "storage_pool_name": "Xiaokang00010's 快乐小站",
            "users": [],
            "modules": []
        }
        file.write(json.dumps(dict))
    printLog(".exmc directory created success.",'i')

with open(core.api.getAbsPath("core/info.json"),'r+') as file:
    storage_info = json.loads(file.read())

# server apis

def syncConfig():
    with open(core.api.getAbsPath('core/info.json'),'w+') as file:
        file.write(json.dumps(storage_info))

def create_account(username:str,password:str):
    password += '_XmediaCenter'
    storage_info['users'].append(
        { 'username': username , 'pwd_encoded':hashlib.md5(password.encode(encoding='utf-8')).hexdigest() }
    )
    syncConfig()

def create_account_with_md5(username:str,password:str):
    storage_info['users'].append(
        { 'username': username , 'pwd_encoded':password }
    )
    syncConfig()

def remove_account(username:str,password:str):
    password += '_XmediaCenter'
    del storage_info['users'][(storage_info['users'].index({ 'username': username , 'pwd_encoded':hashlib.md5(password.encode(encoding='utf-8')).hexdigest() }))]
    syncConfig()

# end of server apis

server_obj = flask.Flask(__name__)

# init flask

session_map = []

@server_obj.route("/")
def idx_of_root():
    return render_template(core.api.getAbsPath(config['default_page_path']))

modules = []
registered_api = {}
registered_path = {}

@server_obj.route("/api",methods=['POST','GET'])
def idx_of_api():
    action = flask.request.args.get('action')
    if action == 'login':
        uinf = flask.request.args.get('userinfo').__str__()
        result = core.xmcp.parseUserInfo(uinf)
        if storage_info['users'].count({ 'username': result['u'], 'pwd_encoded': result['p'] }) == 0:
            return json.dumps({ 'status':'error','reason':'Invalid username or password' })
        idx = storage_info['users'].index({ 'username': result['u'], 'pwd_encoded': result['p'] })
        flask.session['userinfo'] = uinf[1:-1]
        #flask.session["time"] = time.time()
        # configure session lifetime
        flask.session.permanent = True
        server_obj.permanent_session_lifetime = 1*60*60
        return json.dumps({ 'status':'success', 'userinfo': flask.session['userinfo']})
    elif action == 'signup':
        uinf = flask.request.args.get('userinfo').__str__()
        core.api.add_to_pool(uinf)
        return json.dumps({'status':'success'})
    elif action == 'accept_register_request':
        idx = flask.request.args.get('idx')
        if idx == None:
            return json.dumps({'status':'error','reason':'Invalid Request'})
        elif flask.session.get('userinfo') == None:
            return json.dumps({'status':'error','reason':'Invalid Session'})
        else:
            dic = core.api.get_register_requests_pool()
            idx = int(idx)
            if idx + 1 > len(dic['file']['requests']):
                return json.dumps({'status':'error','reason':'Invalid Request'})
            userinfo = dic['file']['requests'][idx]
            if userinfo == None:
                return json.dumps({'status':'error','reason':'Invalid Request'})
            user = core.xmcp.parseUserInfo(userinfo)
            create_account_with_md5(user['u'],user['p'])
            del dic['file']['requests'][idx]
            return core.api.sync_register_requests_pool(dic['file'])
    elif action == 'deny_register_request':
        idx = flask.request.args.get('idx')
        if idx == None:
            return json.dumps({'status':'error','reason':'Invalid Request'})
        elif flask.session.get('userinfo') == None:
            return json.dumps({'status':'error','reason':'Invalid Session'})
        dic = core.api.get_register_requests_pool()
        idx = int(idx)
        if idx + 1 > len(dic['file']['requests']):
            return json.dumps({'status':'error','reason':'Invalid Request'})
        del dic['file']['requests'][idx]
        return core.api.sync_register_requests_pool(dic['file'])
    elif action == 'checker':
        if flask.session.get('userinfo') == None:
            return json.dumps({ 'status':'error','reason':'Invalid Session' })
        return json.dumps({ 'status':'success', 'userinfo': flask.session['userinfo']})
    elif action == "logout":
        flask.session.clear()
        return flask.redirect('/main')
    elif registered_api.get(action) != None:
        return modules[registered_api.get(action)].api_request(flask.request)
    else:
        return "no response"

# module apis

def wdnmd():
    return modules

def load_all_modules():
    print('get called')
    for i in storage_info['modules']:
        modules.append(importlib.import_module('core.plugins.' + i + '.main'))
        modules[-1].requestCPR = wdnmd
        register_obj = modules[-1].register(server_obj)
        if type(register_obj).__name__ == 'dict':
            if register_obj.get('registered_api') != None:
                for j in register_obj.get('registered_api'):
                    registered_api[j] = len(modules)-1
            
        else:
            printLog('core.plugins.' +i + '.main.register() is a bad function.','e')

# end of module apis

def run():
    status = "running"
    server_obj.config['SECRET_KEY'] = '_XmediaCenter_' + str(os.urandom(114514))
    server_obj.session_cookie_name = 'XmediaCenterSession'
    #print(core.xmcp.makeUserInfomation(storage_info['users'][0]))
    load_all_modules()
    server_obj.run(host=config['host'],port=config['port'])
    status = "stopped"