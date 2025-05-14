import re
from typing import List
from classes.TuitionChannel import TUITION_CHANNEL_LIST, TuitionChannel

class TuitionJob():

    # Idea: simply create the object and populate it's fields by extracting info from the message within this constructor
    # IMPORTANT: some details will NOT be extracted as they can simply be directly matched against regex with the whole message.
    def __init__(self, message:str, channel_name:str):

        # store original message
        self.message = message
        
        # placeholders
        self.suitable_tutors:List = []

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
    test = TuitionJob("test msg1","non-existent channel")
    test = TuitionJob("test msg2","Tuition Assignments Singapore - SG Tuition Jobs / SG Tuition Assignments")
        