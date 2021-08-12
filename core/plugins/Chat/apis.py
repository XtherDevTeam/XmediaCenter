import websockets
import core.api
import core.xmcp
import SimpleWebSocketServer
import queue
import threading
import json
import os

def init_info_file():
    if os.access(os.getcwd() + '/core/plugins/Chat/info.json', os.F_OK):
        return
    else:
        with open(os.getcwd() + '/core/plugins/Chat/info.json', 'w+') as file:
            file.write(json.dumps({'groups': [], 'users': {}}))  # groups

def get_info_file():
    with open(os.getcwd() + '/core/plugins/Chat/info.json', 'r+') as file:
        return json.loads(file.read())

class WebSocketsServer(SimpleWebSocketServer.WebSocket):
    def handleMessage(self):
        self.server.data_queue.put(['msg', self.address, self.data])
        print('msg get')

    def handleConnected(self):
        self.server.data_queue.put(['connected', self.address])
        print(self.address, 'get connection')

    def handleClose(self):
        self.server.data_queue.put(['lost', self.address])
        print(self.address, 'lost connection')

class ChatroomServer(object):
    def __init__(self, port):
        self.msg_group={}
        init_info_file()
        group_info=get_info_file()
        for i in group_info['groups']:
            self.msg_group[i]=[]

        self.server=SimpleWebSocketServer.SimpleWebSocketServer(
            '', port, WebSocketsServer)
        self.server.data_queue=queue.Queue(1000)
        self.server_thread=None

    def refresh_msg_group(self):
        group_info=get_info_file()
        for i in group_info['groups']:
            if self.msg_group.get(i) == None:
                self.msg_group[i]=[]
        for i in self.msg_group:
            if group_info['groups'].count(i) == 0:
                del i

    def run(self):
        self.server_thread=threading.Thread(target=self.run_server)
        self.server_thread.start()
        self.main_thread=threading.Thread(target=self.main_process)
        self.main_thread.start()

    def run_server(self):
        self.server.serveforever()

    def push_message(self, msg:list):
        for i in self.msg_group[msg['group']]:
            for key, client in self.server.connections.items():
                if client.address == i:
                    client.send(json.dumps(msg))

    def main_process(self):
        while True:
            if not self.server.data_queue.empty():
                message=self.server.data_queue.get()
                if message[0] == 'msg':
                    print(message[1], 'message get', message[2])
                    print(type(message[1]))
                    for key, client in self.server.connections.items():
                        if client.address == message[1]:
                            msg=json.loads(message[2])
                            if msg.get('userinfo') == None:
                                client.sendMessage(json.dumps(
                                    {'status': 'error', 'reason': 'Invalid Session'}))
                            elif msg.get('group') == None:
                                client.sendMessage(json.dumps(
                                    {'status': 'error', 'reason': 'Invalid group'}))
                            elif msg.get('msg') == None:
                                client.sendMessage(json.dumps(
                                    {'status': 'error', 'reason': 'Invalid Message'}))
                            else:
                                if msg['msg'] == 'join':
                                    self.msg_group[msg['group']].append(
                                        client.address)
                                if self.msg_group.get(msg['group']) == None:
                                    self.msg_group[msg['group']]=[]
                                self.push_message(msg)
                elif message[0] == 'lost':
                    for key, i in self.msg_group:
                        if i.count(message[0]):
                            del i[i.index(message[0])]

server=ChatroomServer(11450)

def get_joined_groups(user: str):
    file = get_info_file()
    if user not in file['users']:
            file['users'][user] = []
    sync_info_file(file)
    return file['users'][user]

def sync_info_file(inf: dict):
    with open(os.getcwd() + '/core/plugins/Chat/info.json', 'w+') as file:
        file.write(json.dumps(inf))
    server.refresh_msg_group()

server.run()
