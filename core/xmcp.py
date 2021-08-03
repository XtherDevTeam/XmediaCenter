import hashlib,json,base64

def makeUserInfomation(username:str,password:str):
    password += '_XmediaCenter'
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
    final = username + ":" + password
    final = str(base64.encodebytes(bytes(final.encode('utf-8'))),encoding='utf-8')
    return final

def makeUserInfomation(uinf:dict):
    final = uinf['username'] + ":" + uinf['pwd_encoded']
    final = str(base64.encodebytes(bytes(final.encode('utf-8'))),encoding='utf-8')
    return final


def makeUserAgent(sid:int,ui:str):
    final = base64.encodebytes((str(sid) + ":" + ui).encode('utf-8'))
    return final.decode('utf-8')

def checkUserAgent(ulist:list,smap:list,ua:str):
    ua = base64.decodebytes(ua.encode('utf-8')).decode('utf-8')
    sid = int(ua[0:ua.find(':')])
    uinf = ua[ua.find(':'):]
    if makeUserInfomation(ulist[smap[sid]]) == uinf:
        return True
    else:
        return False

# return a dict like { 'u':name,'p':pwd_encoded }
def parseUserInfo(ui:str):
    ui = base64.decodebytes(ui.encode('utf-8')).decode('utf-8')
    un = ui[0:ui.find(':')]
    up = ui[ui.find(':')+1:]
    return { 'u':un,'p':up }