# A seperate file to store user configurable values
import os

HostKey = "{IDENTIFIER-HOST}" # String the client should look for
ClientKey = "{IDENTIFIER-CLIENT}" # String the host should look for
language_val = "de_DE" # Language the recording is in
exitWord = ['quit', 'exit', 'stop'] # Words to exit the programm
serialcom = {"port":"COM5","baud":"9600"} # Serial configuration
audio_dict = {"ExtraIdentifierFuerTest89":"test.mp3"} # custom AudioIdentifier:FileName.mp3 in ./audio (! No whitespace)
magic = "guten tag" # Word to recognize

# Automatic generation of AudioIdentifier for files in ./audio
os.chdir("./audio")
for file in os.listdir("."):
    audio_dict[file[:-4]] = file

# System specific configuration preventing manual change when coding on different device
if os.name == "posix":
    print("System: " + os.name)
    serialcom["port"] = "/dev/ttyUSB0"
    for value in audio_dict.keys():
        print(value)
        audio_dict[value] = os.getcwd()+"/"+audio_dict[value] # Total path to audio files
    
elif os.name == "nt":
    print("System: " + os.name)
    serialcom["port"] = "COM7"
    for value in audio_dict.keys():
        audio_dict[value] = os.getcwd()+"\\"+audio_dict[value] # Total path to audio files

print(audio_dict)