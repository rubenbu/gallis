# -*- coding: utf-8 -*-
import SocketServer
import json 
import datetime
import re
 
"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""
 
messages = []
usernames = []
clients = []
helptext = 'Username must consist of A-Z, a-z and 0-9.\n\nType names to list all users.\nType logout to logout.\nType login to login.'
 
class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """
 
    loggedIn = False
    username = ''
 
    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        #
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request
        clients.append(self)
 
        # Loop that listens for messages from the client
        while True:
            #Saving received string as variable
            received_string = self.connection.recv(4096)
            
            #Decoding json string
            message = json.loads(received_string)
            #Save value of key 'request' in variable request
            request = message['request']
 
 
            #Check request for specific key. Do appropriate action.
            if request == 'login':
                if not self.loggedIn:
                    content = message['content']
                    if content in usernames:
                        self.send_error('Username already taken.')
                    elif not self.valid_username(content):
                        self.send_error('Invalid username. Use a combination of A-Z, a-z and 0-9.')
                    else:
                        self.username = content
                        usernames.append(self.username)
                        self.loggedIn = True
                        self.send_info('Login successful.')
                        self.send_history()
                        print 'User' + self.username + ' logged in.'
                else:
                    self.send_error('You are already logged in.')
 
 
            elif request == 'logout':
                if not self.loggedIn:
                    self.send_error('You are not logged in.')
                else:
                    self.send_info('You successfully logged out.')
                    print 'User ' + self.username + ' logged out.'
                    if self.username in usernames:
                        usernames.remove(self.username)
                    self.username = ''
                    self.loggedIn = False
 
 
            elif request == 'msg':
                if self.loggedIn:
                    response = self.create_message(message['content'])
                    messages.append(response)
 
                    for c in clients:
                        if c.loggedIn:
                            c.connection.send(response)
 
                    decodedResponse = json.loads(response)
                    print decodedResponse['timestamp'] + ' ' + decodedResponse['sender'] + ': ' + decodedResponse['content']
                else:
                    self.send_error('You are not logged in.')
 
 
            elif request == 'names':
                if self.loggedIn:
                    self.send_info('Connected users: ' + ', '.join(usernames))
                else:
                    self.send_error('Please log in to see who are logged in.')
 
 
            elif request == 'help':
                self.send_info(helptext)
 
 
            else:
                self.send_error('Invalid request.')
 
 
 
    def send_error(self, message):
        payload = {'timestamp':get_timestamp(),'sender':'server','response':'error','content':message}
        self.connection.send(json.dumps(payload))
 
 
    def send_info(self, message):
        payload = {'timestamp':get_timestamp(),'sender':'server','response':'info','content':message}
        self.connection.send(json.dumps(payload))
 
 
    def send_history(self):
        #messageLength = len(messages)
        #for i in xrange(0,messageLength, 5):
        payload = {'timestamp':get_timestamp(),'sender':'server','response':'history','content':messages}
        self.connection.send(json.dumps(payload))
 
 
    def valid_username(self, username):
        return True if re.match('^[A-Za-z0-9]+$', username) else False
 
 
    def create_message(self, content):
        payload = {'timestamp':get_timestamp(),'sender':self.username,'response':'message','content':content}
        return json.dumps(payload)
 
 
    def finish(self):
        if self.username in usernames:
            usernames.remove(self.username)
        if self in clients:
            clients.remove(self)
 
#Use datetime to give timestamp when chatting
def get_timestamp():
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
 
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.
 
    No alterations are necessary
    """
    allow_reuse_address = True
 
if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.
 
    No alterations are necessary
    """
    HOST, PORT = '', 9998
    print 'Server running...'
 
    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
