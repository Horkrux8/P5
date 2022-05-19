# A separate file to store user configurable values
import os

HostKey = "{IDENTIFIER-HOST}" # String the client should look for
ClientKey = "{IDENTIFIER-CLIENT}" # String the host should look for
language_val = "de_DE" # Language the recording is in
exitWord = ['quit', 'exit', 'stop'] # Words to exit the program
serialcom = {"port":"COM5","baud":"9600"} # Serial configuration
audio_dict = {"test":"test","guten_tag":"guten_tag"} # AudioIdentifier:FileName in ./audio (! No whitespace)
magic = "guten tag" # Word to recognize

# System specific configuration preventing manual change when coding on different device
if os.name == "posix":
    print("System: " + os.name)
    serialcom["port"] = "/dev/ttyUSB0"
    for value in audio_dict.keys():
        audio_dict[value] = os.getcwd()+"/audio/"+audio_dict[value]+".mp3" # Total path to audio files
    
elif os.name == "nt":
    print("System: " + os.name)
    serialcom["port"] = "COM5"
    for value in audio_dict.keys():
        audio_dict[value] = os.getcwd()+"\\audio\\"+audio_dict[value]+".mp3" # Total path to audio files