import re
from typing import List
from src.classes.Tutor import Tutor

GENDERS_I_KNOW = ["male","female","non-binary"]

stevonnie = Tutor(
    name="Stevonnie",
    telegram_handle="@stevonnie",
    address="The beach",
    experience=["Student"],
    gender="non-binary",
    subjects=[
            "math",
            "science",
            "physics",
            "chemistry",
            "english"])

def check_gender(gender:str,message:str) -> bool:

    # what i obeserved: if NO genders were mentioned within the message, then gender does not matter, and pass it as true.
    # however, if they DID specify a gender, then i need to do a check of the genders and see if my gender matches the preferences

    genders_regex = "|".join(GENDERS_I_KNOW)
    preferred_genders = re.findall(genders_regex,message,flags=re.IGNORECASE)
    if (len(preferred_genders) > 0):
        print(f"Student prefers the following genders: {preferred_genders}")
        if gender in preferred_genders:
            print(f"✅ Gender of tutor [{gender}] matches with gender preferences [{preferred_genders}]")
            return True
        else:
            print(f"❌ Gender of tutor [{gender}] do not match with gender preferences [{preferred_genders}]")
            return False
    else:
        print("✅ Student has no gender preference")
        return True
    
if (__name__ == "__main__"):
    msg1 = "asdfasdfasdf no gender preference"
    msg2 = "asdfasdfasd i want males"
    msg3 = "asdfasdf i want female only"
    msg4 = "for some reason i only fw non-binary tutors"
    check_gender(stevonnie.gender,msg1)
    check_gender(stevonnie.gender,msg2)
    check_gender(stevonnie.gender,msg3)
    check_gender(stevonnie.gender,msg4)

    test = "Female"
    print(re.findall(r"male|female",test,flags=re.IGNORECASE))
