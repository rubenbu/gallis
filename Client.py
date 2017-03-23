# -*- coding: utf-8 -*-
import socket
import json
import sys
import time
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
            self.connection.connect((self.host, self.server_port)) #Connect to server
            print 'Successfully connected to the server.'             
        except socket.error as e:  #If connection fails
            print "Failed to connect to server. \nError message:", e
         
         
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
 
    def send_payload(self, data): #Def the different responses
        if data == 'help':
            payload = {'request':'help', 'content': None}
        elif data == None:
                return 0
        elif data == 'names':
            payload = {'request':'names', 'content': None}
        elif data == 'logout':
            payload = {'request':'logout', 'content': None}
            self.loggedon = False
        elif data == 'disconnect':
            return 0
        else:
            if self.loggedon == False:
                payload = {'request':'login', 'content': data}
                self.loggedon = True
 
            else:
                payload = {'request':'msg','content': data}
 
        self.connection.send(json.dumps(payload))
        return 1
         
 
def clientScript(client):
    acceptedResponses = ['error','info','message','history']
    timeCounter = 0
     
    while 1: #Running the chat until the user disconnects
        data = raw_input()
        if data == 'disconnect':
            client.disconnect()
        client.send_payload(data)
 
 
if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.
 
    No alterations are necessary
    """
    client = Client('localhost', 9998)
    clientScript(client)
