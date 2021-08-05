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

def getAbsPath(path:str):
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
    #print(stk.empty())
    while stk.empty():
        temp = stk.top() + '/' + temp
        stk.pop()

    return temp[0:-1]

import hashlib,base64

