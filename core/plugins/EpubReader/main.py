import mimetypes
from types import CodeType
from typing import final
from xml.etree.ElementTree import ElementTree
import flask,core.plugins.FileManager.file_manage,core.api,core.xmcp
from flask.wrappers import Response
from flask.helpers import make_response
from flask.globals import g
from flask.templating import render_template
import json
import core.plugins.EpubReader.epub_parser

name = 'Book Reader'

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
            pass
        else:
            ret.append([path,i.name])
    return ret

def api_request(request:flask.request):
    epub_path = request.args.get('epub')
    epub_path = core.api.getAbsPath(epub_path)
    result = core.plugins.EpubReader.epub_parser.parse('core/storage/'+epub_path)
    if epub_path == None:
        return {'status':'error','reason':'No epub file selected'}
    if type(request.args.get('request')).__name__ == 'str' and request.args.get('request') == 'get_epub_detail':
        return {'path': epub_path, 'title': result['title'], 'author': result['author'], 'chapters': result['chapters']}
    if type(request.args.get('request')).__name__ == 'str' and request.args.get('request') == 'get_file_in_epub':
        file = request.args.get('file')
        if file == None:
            return {'status':'error','reason':'Filename is null'}
        if result['files'].get(file) == None:
            return {'status':'error','reason':'File not exist'}
        return Response( result['files'][core.api.getAbsPath(file)], mimetype=mimetypes.guess_type( file )[0] )
    if type(request.args.get('request')).__name__ == 'str' and request.args.get('request') == 'get_filelist':
        finalresult = []
        for i in result['files']:
            finalresult.append(i)
        return {'filelist':finalresult}
    if type(request.args.get('request')).__name__ == 'str' and request.args.get('request') == 'get_iframe_object':
        file = request.args.get('file')
        file = core.api.getAbsPath(file)
        if file == None:
            return {'status':'error','reason':'Filename is null'}
        if result['files'].get(file) == None:
            return {'status':'error','reason':'File not exist'}
        if mimetypes.guess_type(file)[0].find('html') == -1:
            return {'status':'error','reason':'Not a current xml file'}
        
        return Response(core.plugins.EpubReader.epub_parser.covertToViewableHtml(result['files'][file],epub_path,file),mimetype='application/xhtml+xml')
    return {'status':'error','reason':'unsupported api'}

def idx_of_epubreader():
    is_logined = flask.session.get('userinfo') != None
    user = {}
    if flask.request.values.get('path') == None:
        return {'status':'error','reason':'path is null'}
    if is_logined:
        user = core.xmcp.parseUserInfo(flask.session.get('userinfo'))
    if flask.request.values.get('index') == None:
        return render_template("plugins_templates/main/index.html",
                                plugins_list=get_plugins_path_list(),
                                renderText=flask.Markup(
                                    render_template(
                                        'plugins_templates/EpubReader/file.html',
                                        is_logined = is_logined,
                                        user = user,
                                        path = core.api.getAbsPath(flask.request.values.get('path')),
                                        book = core.plugins.EpubReader.epub_parser.parse('core/storage/'+core.api.getAbsPath(flask.request.values.get('path'))),
                                    )
                                ))
    else:
        return render_template("plugins_templates/main/index.html",
                                plugins_list=get_plugins_path_list(),
                                renderText=flask.Markup(
                                    render_template(
                                        'plugins_templates/EpubReader/indexing.html',
                                        is_logined = is_logined,
                                        user = user,
                                        path = core.api.getAbsPath(flask.request.values.get('path')),
                                        book = core.plugins.EpubReader.epub_parser.parse('core/storage/'+core.api.getAbsPath(flask.request.values.get('path'))),
                                        now_index = int(flask.request.values.get('index')),
                                        total_index = len(core.plugins.EpubReader.epub_parser.parse('core/storage/'+core.api.getAbsPath(flask.request.values.get('path')))['files']),
                                    )
                                ))

def register(server:flask.Flask):
    #print(requestCPR)
    server.add_url_rule('/reader',view_func=idx_of_epubreader)
    return {
        'registered_api': ['epub_api']
    }