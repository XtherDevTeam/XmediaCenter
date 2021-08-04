import os,sys,json,core.api,flask

def is_directory(path:str):
    if path[0] == '"':
        path = path[1:-1]
    return os.path.isdir('core/storage/' + core.api.getAbsPath(path))

def response_with_file(path):
    if path[0] == '"':
        path = path[1:-1]
    try:
        return flask.send_file(os.getcwd()+'/core/storage/' + core.api.getAbsPath(path),as_attachment=True)
    except Exception as e:
        return json.dumps({ 'status':'error','reason':'Failed:' + str(e) })

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