

class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
	    # TODO: More key:values pairs are needed	
        }

    def parse(self, payload):
        payload = # TODO:decode the JSON object

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            # TODO: Response not valid

    def parse_error(self, payload):
    
    def parse_info(self, payload):
    
    #TODO: Include more methods for handling the different responses... 
