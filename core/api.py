import json
import base64
import hashlib
from os import F_OK, access


class Stack(object):

    def __init__(self):
        self.stack = []

    def push(self, data):
        self.stack.append(data)

    def pop(self):
        return self.stack.pop()

    def top(self):
        return self.stack[-1]

    def empty(self):
        return len(self.stack)


def getAbsPath(path: str):
    if path == None:
        return ''
    if path != '' and path[0] == '"':
        path = path[1:-1]
    stk = Stack()
    temp = ''
    for i in path:
        if i == '/' or i == '\\':
            if temp == '':
                continue
            elif temp == '..':
                stk.pop()
            elif temp == '.':
                temp == ''
            else:
                stk.push(temp)
            temp = ''
            continue
        else:
            temp += i

    stk.push(temp)
    temp = ''
    # print(stk.empty())
    while stk.empty():
        temp = stk.top() + '/' + temp
        stk.pop()

    return temp[0:-1]


def get_filename(path: str):
    if path == None:
        return ''
    if path != '' and path[0] == '"':
        path = path[1:-1]
    stk = Stack()
    temp = ''
    for i in path:
        if i == '/' or i == '\\':
            if temp == '':
                continue
            elif temp == '..':
                stk.pop()
            elif temp == '.':
                temp == ''
            else:
                stk.push(temp)
            temp = ''
            continue
        else:
            temp += i

    return temp


def init_register_request_pool():
    if access('register_request_pool.json', F_OK):
        return
    with open('register_request_pool.json', 'w+') as file:
        print(json.dumps( { 'name':'register_request_pool', 'requests': [] } ))
        file.write(json.dumps({ 'name':'register_request_pool', 'requests': [] }))
    return


def add_to_pool(uinf: str):
    init_register_request_pool()
    js = {}
    with open('register_request_pool.json', 'r+') as file:
        js = json.loads(file.read())
        js['requests'].append(uinf)
    with open('register_request_pool.json','w+') as file2:
        file2.write(json.dumps(js))
    return



def get_register_requests_pool():
    try:
        with open('register_request_pool.json', 'r+') as file:
            js = json.loads(file.read())
            return {'status':'success','file':js}
    except Exception as e:
        return {'status':'error','reason':e.__str__()}

def sync_register_requests_pool(dic:dict):
    try:
        with open('register_request_pool.json', 'w+') as file:
            file.write(json.dumps(dic))
            return {'status':'success'}
    except Exception as e:
        return {'status':'error','reason':e.__str__()}