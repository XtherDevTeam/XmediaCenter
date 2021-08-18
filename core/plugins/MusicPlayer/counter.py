import json,os,sys,hashlib

def init_counter_file(userinfo:str):
    if os.access(os.getcwd() + '/core/plugins/MusicPlayer/.musicplayer/counter-' + hashlib.md5(userinfo.encode('utf-8')).hexdigest() + '.json',os.F_OK):
        None
    else:
        print(json.dumps( { 'type':'Music Counter','content':{} } ))
        with open(os.getcwd() + '/core/plugins/MusicPlayer/.musicplayer/counter-' + hashlib.md5(userinfo.encode('utf-8')).hexdigest() + '.json','w+') as file:
            file.write(json.dumps( { 'type':'Music Counter','content':{} } ))
            print('你妈什么时候死啊')

def get_counter_file(userinfo:str):
    init_counter_file(userinfo)
    if userinfo == None or userinfo == '':
        return {'status':'error','reason':'Invalid Session'}
    try:
        with open('core/plugins/MusicPlayer/.musicplayer/counter-' + hashlib.md5(userinfo.encode('utf-8')).hexdigest() + '.json','r+',encoding='utf-8') as file:
            return {'status':'success','counter':json.loads(file.read())}
    except Exception as e:
        return {'status':'error','reason':str(e)}

def sync_counter_file(userinfo:str,file_:dict):
    print(file_)
    init_counter_file(userinfo)
    try:
        with open(os.getcwd() + '/core/plugins/MusicPlayer/.musicplayer/counter-' + hashlib.md5(userinfo.encode('utf-8')).hexdigest() + '.json','w+') as file:
            file.write(json.dumps( file_ ))
        return {'status':'success'}
    except Exception as e:
        return {'status':'error','reason':str(e)}

# song : song title
def update_counter_file(userinfo:str,song:str):
    init_counter_file(userinfo)
    file = get_counter_file(userinfo)
    if file['status'] == 'error':
        return file
    file = file['counter']
    if file['content'].get(song) == None:
        file['content'][song] = 0
    file['content'][song] += 1
    return sync_counter_file(userinfo,file)

def get_program_readable_counter_data(userinfo:str):
    if userinfo == None:
        return []
    file = get_counter_file(userinfo)
    if file['status'] == 'error':
        return file
    file = file['counter']['content']
    result = []
    for key in file:
        result.append( [ key , file[key] ] )
    result.sort()
    return result