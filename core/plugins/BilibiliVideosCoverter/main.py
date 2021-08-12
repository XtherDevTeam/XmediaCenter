from types import CodeType
import flask,core.plugins.FileManager.file_manage,core.api,core.xmcp,os
from flask.globals import g
from flask.templating import render_template
import json

name = 'BilibiliVideosCoverter'

requestCPR = None

def cross_plugin_request(args:list):
    return 'denied'

def get_plugins_path_list():
    ret = []
    #print(requestCPR())
    for i in requestCPR():
        if i.name == name:
            continue
        path = i.cross_plugin_request([ 'get_path' ])
        if type(path).__name__ == 'str' and path == 'denied':
            print('failed with denied')
        else:
            ret.append([path,i.name])
    return ret

def api_request(request:flask.request):
    request_video_path = request.values.get('path')
    coverted_video_path = request_video_path[0:-4] + '.encoded.mp4'
    request_video_path = '"'+ os.getcwd() + '/core/storage/' + core.api.getAbsPath(request_video_path) + '"'
    coverted_video_path = '"' + os.getcwd() + '/core/storage/' + core.api.getAbsPath(coverted_video_path) + '"'
    fp = os.popen('ffmpeg -i ' + request_video_path + ' ' + coverted_video_path,'r')
    str = ''
    while True:
        str = fp.readline()
        if str == '':
            break
        str = str.replace('\n','')
        print(str,end='')
        for i in str:
            print('\b',end='')
        print('\b',end='')
    fp.close()
    request_video_path = request_video_path[1:-1]
    coverted_video_path = coverted_video_path[1:-1]
    os.remove(request_video_path) # remove old file
    os.rename(coverted_video_path,request_video_path) # replace old file

    return json.dumps({'status':'success'})

def register(server:flask.Flask):
    return {
        'registered_api': ['video_covert_api']
    }