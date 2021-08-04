import os,sys,json,core.api,flask

def get_file_list(path):
    return os.listdir('core/storage/' + core.api.getAbsPath(path))

def response_with_file(path):
    if path[0] == '"':
        path = path[1:-1]
    try:
        return flask.send_file(os.getcwd()+'/core/storage/' + core.api.getAbsPath(path),as_attachment=True)
    except Exception as e:
        return json.dumps({ 'status':'error','reason':'Failed:' + str(e) })