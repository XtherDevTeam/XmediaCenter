import os,sys,json,core.api,flask,shutil
from posixpath import expanduser

def is_directory(path:str):
    if path[0] == '"':
        path = path[1:-1]
    return os.path.isdir('core/storage/' + core.api.getAbsPath(path))

def response_with_file(path):
    if path != None and path[0] == '"':
        path = path[1:-1]
    try:
        return flask.send_file(os.getcwd()+'/core/storage/' + core.api.getAbsPath(path),as_attachment=True)
    except Exception as e:
        return json.dumps({ 'status':'error','reason':'Failed:' + str(e) })

def create_dir(path):
    if path != None and path[0] == '"':
        path = path[1:-1]
    if path == None:
        return json.dumps({ 'status':'error','reason':'empty argument detected' })
    try:
        os.mkdir('core/storage/' + core.api.getAbsPath(path))
        return json.dumps({ 'status':'success' })
    except Exception as e:
        return json.dumps({ 'status':'error','reason':str(e) })
def get_file_list(path):
    if path != '' and path[0] == '"':
        path = path[1:-1]
    not_modified = os.listdir('core/storage/' + core.api.getAbsPath(path))
    final = []
    for i in not_modified:
        if is_directory(core.api.getAbsPath(path+'/'+i)):
            final.append( { 'filename':i,'type':'dir' } )
        else:
            final.append( { 'filename':i,'type':'file' } )
    return final

def remove(path):
    if path != '' and path[0] == '"':
        path = path[1:-1]
    if path == None:
        return json.dumps({ 'status':'error','reason':'empty path detected' })
    try:
        if is_directory(path):
            shutil.rmtree('core/storage/' + core.api.getAbsPath(path))
        else:
            os.remove('core/storage/' + core.api.getAbsPath(path))
        return json.dumps({ 'status':'success' })
    except Exception as e:
        return json.dumps({ 'status':'error','reason':str(e) })

def rename(path,newname):
    if path != '' and path[0] == '"':
        path = path[1:-1]
    if path == None:
        return json.dumps({ 'status':'error','reason':'empty path detected' })
    if newname != '' and newname[0] == '"':
        newname = newname[1:-1]
    if newname == None:
        return json.dumps({ 'status':'error','reason':'empty path detected' })
    try:
        os.rename('core/storage/' + core.api.getAbsPath(path),'core/storage/' + core.api.getAbsPath(newname))
        return json.dumps({ 'status':'success' })
    except Exception as e:
        return json.dumps({ 'status':'error','reason':str(e) })