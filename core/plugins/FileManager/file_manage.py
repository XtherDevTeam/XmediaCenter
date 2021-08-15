import os,sys,json,core.api,flask,shutil,magic
from posixpath import expanduser

def is_directory(path:str):
    if path[0] == '"':
        path = path[1:-1]
    return os.path.isdir('core/storage/' + core.api.getAbsPath(path))

def response_with_file(path,request:flask.request):
    if path != None and path[0] == '"':
        path = path[1:-1]
    try:
        is_preview = True
        if magic.from_file(os.getcwd()+'/core/storage/' + core.api.getAbsPath(path),mime=True) == 'application/octet-stream':
            is_preview = False
        else:
            is_preview = True
        
        if request.headers.get('Range') != None:
            startIndex = 0
            part_length = 2 * 1024 * 1024
            print(request.headers.get('Range')[request.headers.get('Range').find('='):request.headers.get('Range').find('-')])
            startIndex = int(request.headers.get('Range')[request.headers.get('Range').find('=')+1:request.headers.get('Range').find('-')])
            endIndex = startIndex + part_length - 1
            fileLength = os.path.getsize(os.getcwd()+'/core/storage/' + core.api.getAbsPath(path))
            
            response_file = bytes()

            with open(os.getcwd()+'/core/storage/' + core.api.getAbsPath(path),'rb') as file:
                file.seek(startIndex)
                response_file = file.read(part_length)

            response = flask.make_response(response_file)

            response.headers['Accept-Ranges'] = 'bytes'
            response.headers['Content-Range'] = 'bytes ' + str(startIndex) + '-' + str(endIndex) + '/' + str(fileLength)
            response.headers['Content-Type'] = magic.from_file(os.getcwd()+'/core/storage/' + core.api.getAbsPath(path),mime=True)

            response.status_code = 206
            return response
        
        return flask.send_file(os.getcwd()+'/core/storage/' + core.api.getAbsPath(path),as_attachment=not is_preview,attachment_filename=core.api.get_filename(path),mimetype=magic.from_file(os.getcwd()+'/core/storage/' + core.api.getAbsPath(path),mime=True))
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
            final.append( { 'filename':i,'type':'file','mime':magic.from_file('core/storage/' + core.api.getAbsPath(path+'/'+i),mime=True) } )
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