# -*- coding: utf-8 -*-
import socket
import sys
import time
import json
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser
 
 
class Client:
    """
    This is the chat client class
    """
 
    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """
        self.loggedon=False
        # Set up the socket connection to the server
        try:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            print "Failed to create socket. Error message:", e
         
        self.host = host
        self.server_port = server_port
        self.lastMessageRecieved = None
        self.parser = MessageParser()
        self.run()
        self.rcv = MessageReceiver(self, self.connection)
        self.rcv.start()
 
    def run(self):
        # Initiate the connection to the server
        try:
            self.connection.connect((self.host, self.server_port))
             
        except socket.error as e:
            print "Failed to connect to server. \nError message:", e
         
        print 'You have successfully connected to the server.'
         
    def disconnect(self):
        try:
            self.connection.close()
            self.loggedon = False
            exit()
        except socket.error as e:
            print "Failed to disconnect from server. Error message:", e
        pass
 
    def receive_message(self, message):
        self.lastMessageRecieved = self.parser.parse(message)
        if self.lastMessageRecieved == 'error':
            self.loggedon = False
 
    def send_payload(self, data):
        if data == 'help':
            toEncode = {'request':'help', 'content': None}
        elif data == None:
                return 0
        elif data == 'names':
            toEncode = {'request':'names', 'content': None}
        elif data == 'logout':
            toEncode = {'request':'logout', 'content': None}
            self.loggedon = False
        elif data == 'disconnect':
            return 0
        else:
            if self.loggedon == False:
                toEncode = {'request':'login', 'content': data}
                self.loggedon = True
 
            else:
                toEncode = {'request':'msg','content': data}
 
        self.connection.send(json.dumps(toEncode))
        return 1
         
 
def clientScript(client):
    acceptedResponses = ['error','info','message','history']
    timeCounter = 0
     
    while 1:
        data = raw_input()
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K")
        if data == 'disconnect':
            client.disconnect()
        client.send_payload(data)
 
 
if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.
 
    No alterations are necessary
    """
    client = Client('129.241.206.199', 9998)
    clientScript(client)
