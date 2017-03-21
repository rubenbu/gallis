# -*- coding: utf-8 -*-
import socket
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser
import json #Need json to parse

class Client:
    """
    This is the chat client class
    """

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # TODO: Finish init process with necessary code
        self.host = host #Set host
        self.server_port = server_port #Set server port
        self.message_parser = MessageParser() #Call parsing method
        #Start message receiver
        self.message_receiver = MessageReceiver(self,self.connection)
        self.run()


    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))

        # Set up dictionary for request and content
        #NB! Dictionaries are unordered in Python
        Client_dict = {
            'login':str,
            'logout':None,
            'msg':str,
            'names':None,
            'help':None
            } 


        #Hilarious welcome messages
        print 'Welcome to this homemade chatting service. It will most certainly fail'
        print 'Press help to get nonexisting assistance.'
        
        #Save user input as variable
        user_input = raw_input('Please get on with your request. Im busy chatting.')

        #Divide user input into request and content. NOT SURE IF THIS DOES THE JOB
        #Indice 0 will be request, 1 content
        split_user_input = user_input.split(",")

        
    def login(self, data):
        #Checks if user input is logging in
        if split_user_input[0] == 'login':
            #log person in
            user = split_user_input[1]
            payload = {'request': 'login', 'content': 'user'}
            #convert dictionary (payload) to json strings
            json_payload = json.dumps(payload)
            #call sending of payload to server
            self.send_payload(json_payload)
        else:
            pass
        
    def disconnect(self):
        if split_user_input[0] == 'logout':
            print 'Disconnection is imminent. See you on the other side.'
            self.connection.close() #Close connection
        else:
            pass
        
        

    def receive_message(self, message):
        #Received message is sent directly to parser class
        self.message_parser.parse(message)

    def send_payload(self, data):
        self.connection.send(data.encode())
        if split_user_input[0] == 'msg':
            #send msg
            msg = split_user_input[1]
            payload = {'request': 'msg', 'content': 'msg'}
            #convert dictionary (payload) to json strings
            json_payload = json.dumps(payload)
            #call sending of payload to server
            #KAN DET UNDER GJØRES? BRUKE EGEN DEL AV METHOD?
            self.send_payload(json_payload)
        else:
            pass
        
    def names(self):
        if split_user_input[0] == 'help':
            #send request to server to receive a list of everyone logged in
            user = split_user_input[1]
            payload = {'request': 'names', 'content': ''}
            #convert dictionary (payload) to json strings
            json_payload = json.dumps(payload)
            #call sending of payload to server
            self.send_payload(json_payload)
        else:
            pass
        

    def help(self):
        if split_user_input[0] == 'help':
            #send request to server to receive a help text containing all requests supported
            user = split_user_input[1]
            payload = {'request': 'help', 'content': ''}
            #convert dictionary (payload) to json strings
            json_payload = json.dumps(payload)
            #call sending of payload to server
            self.send_payload(json_payload)
        else:
            pass

    


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)
