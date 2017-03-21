# -*- coding: utf-8 -*-
from threading import Thread
import json

class MessageReceiver(Thread):
    """
    This is the message receiver class. The class inherits Thread, something that
    is necessary to make the MessageReceiver start a new thread, and it allows
    the chat client to both send and receive messages at the same time
    """

    def __init__(self, client, connection):
        """
        This method is executed when creating a new MessageReceiver object
        """

        # Flag to run thread as a deamon
        self.daemon = True
        
        # TODO: Finish initialization of MessageReceiver
        self.connection = connnect
        self.client = client
        self.start()



    def run(self):
            while True:
            payload = self.connection.recv(4096).decode()
            self.client.receive_message(payload)
            pass


