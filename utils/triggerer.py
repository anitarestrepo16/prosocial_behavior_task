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
        self.trigger_labels_to_send = {}
        self.trigger_labels_received = {}
    
    def set_trigger_labels(self, trigger_types):
        '''
        Map the trigger_types (list of strings with the labels for the flags)
        onto pin settings.
        Input:
            trigger_types (lst): list of strings with the text labels for the flags
        Output: list of integers representing the unique pin settings that need to be sent
            to the Bionex for each trigger type.
        '''
        # ensure trigger_types has 127 or fewer items b/c max unique combinations given mindware
        assert len(trigger_types) <= 127, 'Max trigger types is 127!'
        for index, trigger in enumerate(trigger_types):
            self.trigger_labels_to_send[trigger] = index + 1
            self.trigger_labels_received[trigger] = map_to_mindware(index + 1)
            

    def send_trigger(self, trigger_type, duration = .002):
        value = self.trigger_labels_to_send[trigger_type]
        self.p.setData(value)
        time.sleep(duration)
        self.p.setData(0)

    def create_txt_file(self, filename):
        '''
        Create the txt file that needs to be read into Biolab in the events tab.
        Input: 
            filename (str): what to name the txt file
        Returns: saves .txt file with the pin numbers that will be received by Mindware
            corresponding to each of the trigger types.
        '''
        assert len(self.trigger_labels_received) > 0, 'Trigger labels have not been set!'
        txt = ''
        for key, val in self.trigger_labels_received.items():
            line = key + '\t' + str(val) + '\n'
            txt += line
        with open(filename + '.txt', 'a') as txt_file:
            txt_file.write(txt)
            

def map_to_mindware(value):
    '''
    Helper function to translate intended pin numbers to the number mindware expects.
    Input:
        value (int): the flag number associated with a specific flag
    Returns (int): the pin setting that needs to be sent for the Bionex to read as the intended
    value.
    '''
    intended = bin(value)[2:]
    actual = intended + '1'
    return int(actual, 2)