import re
from classes.TuitionChannel import TUITION_CHANNEL_LIST, TuitionChannel
from classes.TuitionJob import TuitionJob


def create_tuition_job(message:str, channel_name:str) -> TuitionJob:
        # using the name of the tuition channel that this message was from, 
        # get the TuitionChannel object, and use that as regex reference when extracting the details of the job.
        tuition_channel:TuitionChannel = None
        for channel in TUITION_CHANNEL_LIST:
            if channel_name == channel.channel_name:
                tuition_channel = channel
                break
        if tuition_channel != None:
            # extract details with given regex. each detail extracted uses a specific function from the details_extractor.py tools file
            print(f"Found tuition channel: {tuition_channel.channel_name}")
            address = extract_address(message,tuition_channel.address_regex)

        else:
            print("⚠️ Error: No tuition channel found for this message.")
        pass

def extract_address(message:str,address_regex:str):
    try:
        # extract address
        address:str = " ".join(re.findall(address_regex,message))
        print(f"Address extracted: {address}")
    except Exception as e:
        print(f"Error occured while extracting address: {e}")
    pass

def extract_experience():
    pass

if __name__ == "__main__":
    print(f"Hello from {__package__}!")

