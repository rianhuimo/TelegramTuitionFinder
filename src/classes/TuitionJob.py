import re
from .SuitableTutor import SuitableTutor
from .TuitionChannel import TUITION_CHANNEL_LIST, TuitionChannel

class TuitionJob():

    # Basic constructor. Called by details_extractor.py
    def __init__(
            self, 
            message:str, 
            address:str, 
            subjects:list[str], 
            subject_levels:list[str], 
            experience:int,
            suitable_tutors:list[SuitableTutor],
            tuition_channel:TuitionChannel):
        
        self.message = message # store original message
        self.address = address
        self.subjects = subjects
        self.subject_levels = subject_levels
        self.experience = experience

        self.suitable_tutors = suitable_tutors
        self.tuition_channel = tuition_channel


    # TODO: delete this old one.
    def __init__(self, message:str, channel_name:str):

        # store original message
        self.message = message
        
        # placeholders
        self.suitable_tutors:list = []

        # get the correct tuition channel to be filtering against
        self.tuition_channel:TuitionChannel = None
        for channel in TUITION_CHANNEL_LIST:
            if channel_name == channel.channel_name:
                self.tuition_channel = channel
                break
        if (self.tuition_channel):
            # print(f"Tuition channel found: {tuition_channel.channel_link}")
            try:
                # extract address
                self.address:str = re.findall(self.tuition_channel.address_filter,message)[0]
                # print(f"Address found: {self.address}")
                # if the address turns out to be online, adjust the value accordingly
                if "online" in self.address.lower():
                    self.address = "online"
            except Exception as e:
                self.address = None
                print(f"Error extracting address:\n{e}")
        else:
            print(f"No match for any tuition channel: {channel_name}")

if (__name__ == "__main__"):
    pass
        