#!/bin/python3
# Import of libraries
from queue import Empty
from time import sleep
import speech_recognition as sr
import serial

# Configuration
r = sr.Recognizer()
m = sr.Microphone()

language_val = "de-DE"
magic = "guten tag"
runmode = 2 # 0 = record / 1 = usepremade audio file / 2 = skip record process
exitWord = ['quit', 'exit']
serialcom = {"port":"/dev/ttyUSB0","baud":"9600"}

def usepremade():
    """Sending an existing recording with the magic word to google for recognition"""
    print("Trying voice recognition with premade file")
    with sr.AudioFile("/home/lennart/piTalk/guten_tag.wav") as source:
        audio = r.record(source)
    reply = r.recognize_google(audio, language=language_val)
    return reply

def record():
    print("Starting voice recognition")
    print("One moment...")
    with m as source: r.adjust_for_ambient_noise(source) # Take ambient noise into account
    while True:
        print("Now Ready, listening in %s. (Press Ctrl+c to or say exit or quit to quit)" % language_val)
        with m as source: audio = r.listen(source)
        print("found audio sample")
        try:
            value = r.recognize_google(audio, language=language_val)
            # decoding google's answer
            if str is bytes:
                reply = "{}".format(value).encode("utf-8")
            else:
                reply = "{}".format(value)
            if reply in exitWord:
                print("Exit word found - bye, bye")
                quit()
            else:
                print("You said: %s" % reply)
        # debugging google errors
        except sr.UnknownValueError:
            print("The Google API could not understand the audio...")
        except sr.RequestError as e:
            print("!")
            #print("Couldn't request results from Google Speech Recognition service; {0}".format(e))
        if reply is not None and not Empty:
            return reply

def openDoor():
    """Send serial message to trigger esp program"""
    print("Sending door opening command over serial")
    port, baud = [value for value in list(serialcom.values())] # Configuring serial
    ser = serial.Serial(port, baud, timeout=1)
    ser.flush()

    ser.write("HOST: {IDENTIFIER-HOST}alalal".encode()) # Send host message
    while True:
        if ser.in_waiting > 0:
            data = ser.readline()#.decode('utf-8').rstrip()
            print(data)
            #if "{IDENTIFIER-CLIENT}" in data: # search for client message in serial com
            #    print("recognized client signal")
            #    ser.close()
            #    break

def main():
    """Decided runmode and string recognition"""
    print("running in mode = %s" % runmode)
    if runmode == 0:
        recstring = record() 
    elif runmode == 1:
        recstring = usepremade()
    elif runmode == 2:
        recstring = magic

    # compare string with the wanted string
    if recstring.lower() == magic.lower():
        print("Magic word recognized = %s" % magic)
        openDoor()
        #os.system("echo 'your command goes here'")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass