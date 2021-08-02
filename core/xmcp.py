import hashlib,json,base64

def makeUserInfomation(username:str,password:str):
    password = hashlib.md5(password.encode('utf-8'))
    final = username + ":" + str(password)
    final = str(base64.encodebytes(bytes(final.encode('utf-8'))),encoding='utf-8')
    return final

def makeUserInfomation(uinf:dict):
    password = hashlib.md5(uinf['pwd_encoded'].encode('utf-8'))
    final = uinf['name'] + ":" + str(password)
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