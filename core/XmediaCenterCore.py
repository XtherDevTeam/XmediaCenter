# Main core

import os,json,sys,flask,api
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
if os.access(api.getAbsPath(config['storage_path'] + '/.exmc'),os.F_OK) == False:
    # first run
    printLog(".exmc path does not exist. will create one",'i')
    os.mkdir(api.getAbsPath(config['storage_path'] + '/.exmc'))
    with open(api.getAbsPath(config['storage_path'] + '/.exmc/info.json'),'w+') as file:
        # default config file template
        dict = {
            "storage_pool_name": "Xiaokang00010's 快乐小站",
            "users": [],
            "modules": []
        }
        file.write(json.dumps(dict).encode(encoding='utf-8'))
    printLog(".exmc directory created success.")

flask = flask.Flask(__name__)

# init flask

session_map = []

@flask.route("/")
def index():
    return render_template(api.getAbsPath(config['default_page_path']))

def run():
    flask.debug = True
    status = "running"
    flask.run(host=config['host'],port=config['port'])