from psychopy.parallel import ParallelPort
import time

class Triggerer():
    '''
    Attributes:
    - trigger_labels: dictionary of trigger types paired with the pin number (1-255)
    Methods:
    - set_trigger_labels: takes a list of strings and pairs them with unique pin numbers
    - send_trigger: takes a trigger type and optional duration parameter and sends a trigger
    (move pin to adequate number and brings it back down after a certain duration (default = .002))
    '''

    def __init__(self, address):
        self.p = ParallelPort(address)
        self.trigger_labels = {}
    
    def set_trigger_labels(self, trigger_types):
        '''
        Map the trigger_types (list of strings with the labels for the flags)
        onto pin settings.
        
        '''
        for index, trigger in enumerate(trigger_types):
            self.trigger_labels[trigger] = index + 1
        return self.trigger_labels
            

    def send_trigger(self, trigger_type, duration = .002):
        value = self.trigger_labels[trigger_type]
        self.p.setData(value)
        time.sleep(duration)
        self.p.setData(0)
