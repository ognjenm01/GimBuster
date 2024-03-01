from util import timestamp

class Subscription:
    def __init__(self, full_name, chat_id, enabled, timestamp):
        self.full_name = full_name
        self.chat_id = chat_id
        self.enabled = enabled
        self.timestamp = timestamp
    
    def enable(self):
        self.enabled = True
        self.timestamp = timestamp()

    def disable(self):
        self.enabled = False
        self.timestamp = timestamp()