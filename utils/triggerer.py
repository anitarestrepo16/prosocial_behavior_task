from psychopy.parallel import ParallelPort
import time

class Triggerer():
    '''
    Attributes:
    - trigger_labels_to_send: dictionary of trigger types (strings) paired with the bit number (1-127) that
     will be sent to Biolab to trigger that flag.
    - trigger_labels_received: dictionary of trigger types (strings) paired with the bit number (1-255,
      odd numbers only) that Biolab will register as belonging to that flag (for stupid reasons of Mindware
      designing the Bionex to communicate with EPrime).
    Methods:
    - set_trigger_labels: Takes a list of strings and pairs them with unique trigger labels 
    (both to send and received). Sets attributes trigger_labels_to_send and trigger_labels_received.
    - send_trigger: takes a trigger type and optional duration parameter and sends a trigger
    (move pins to adequate bit number and brings them back down after a certain duration (default = .002s))
    - create_txt_file: Create the txt file that needs to be read into Biolab in the events tab.
    '''

    def __init__(self, address):
        self.p = ParallelPort(address)
        self.trigger_labels_to_send = {}
        self.trigger_labels_received = {}
    
    def set_trigger_labels(self, trigger_types):
        '''
        Takes a list of strings and pairs them with unique trigger labels (both to send and received). Sets
            attributes trigger_labels_to_send and trigger_labels_received.
        Input:
            trigger_types (lst): list of strings with the text labels for the flags
        Output: None
        '''
        # ensure trigger_types has 127 or fewer items b/c max unique combinations given mindware
        assert len(trigger_types) <= 127, 'Max trigger types is 127!'
        for index, trigger in enumerate(trigger_types):
            self.trigger_labels_to_send[trigger] = index + 1
            self.trigger_labels_received[trigger] = map_to_mindware(index + 1)
            

    def send_trigger(self, trigger_type, duration = .002):
        '''
        Takes a trigger type and optional duration parameter and sends a trigger (move pins to 
            adequate bit number and brings them back down after a certain duration (default = .002s))
        Inputs:
            trigger_type (str): trigger label to send
            duration (float): optional
        Output: None
        '''
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