import json

class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'message': self.parse_message,
            'history': self.parse_history
        }

    def parse(self, payload):
        payload = json.loads(payload) # TODO:decode the JSON object

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            print payload
            print 'Not valid'
            return 'invalid'

    def parse_error(self, payload):
		print 'Error'
		print payload['content']
		return 'error'
    
def parse_info(self, payload):
        print payload['content']
        return payload['content']
    
    def parse_message(self, payload):
	print payload['timestamp'],' - ',payload['sender'], ': ',payload['content']
        return 'message'

    def parse_history(self, payload):
        print 'Previously sent message: '
        PrevMes = payload['content']
        for elem in PrevMes:
            message=json.loads(elem)
            print message['timestamp'],' - ',message['sender'], ': ', message['content']
        return 'history'
