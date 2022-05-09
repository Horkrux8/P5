#!/bin/python3
# Import of libraries
from gtts import gTTS
import speech_recognition as sr
import serial
import config as c

# Configuration
recognizer = sr.Recognizer()
microphone = sr.Microphone()
port, baud = [value for value in list(c.serialcom.values())]
ser = serial.Serial(port, baud, timeout=1)
ser.flush()
print("Libraries Initialized")

runmode = 3 # 1 = record / 2 = skip record process / 3 = configure servo

def record():
    """Sending a new voice sample with magic word to google for recognition"""
    print("Starting voice recognition")
    print("One moment...")
    with microphone as source: recognizer.adjust_for_ambient_noise(source) # Take ambient noise into account
    while True:
        print("Now Ready, listening in %s. (Press Ctrl+c to or say exit/quit/stop to quit)" % c.language_val)
        with microphone as source: audio = recognizer.listen(source) # m is microphone (see configuration)
        print("found audio sample")
        try:
            value = recognizer.recognize_google(audio, language=c.language_val)
            # Decoding google's answer if encoded
            if str is bytes:
                reply = "{}".format(value).encode("utf-8")
            else:
                reply = "{}".format(value)
            
            print("You said: %s" % reply)
            return reply

        # Handling google reply error
        except sr.UnknownValueError:
            print("The Google API could not understand the audio...")

def play(play_string):
    """Play the given or audio associate with the string"""
    print(c.audio_dict)
    if play_string in c.audio_dict.keys():
        # Play one of the audios defined in config
        print("Found existing audio")
        c.os.system("mpg123 -q " + c.audio_dict[play_string])
    else:
        # Create new audio by google
        print("Creating temporary audio")
        file = play_string+".mp3"
        tts = gTTS(play_string, c.language_val[0:2]) # Take first two char from language_val (de)_DE
        tts.save(file)
        # Play audio using command line player
        c.os.system("mpg123 -q " + file)
        #c.os.system("rm " + file)
    print("Said %s" % play_string)


def send(Send_string):
    """Send the given String over serial with identifier"""
    ser.write((c.HostKey+str(Send_string)).encode())
    #print("HOST Send: %s %s" % c.HostKey, Send_string)

def receive(Search_string):
    """Read serial and search for the given String"""
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').rstrip()
            print("HOST Received: %s" % data)
            if Search_string in data:
                print("HOST found: %s" % Search_string)
                return data


def configureServo():
    """Continuosly change servo by userinput"""
    while True:
        print("Enter degree")
        send(input())
        print(receive(c.ClientKey))

def main():
    """Decided runmode and string recognition"""
    print("running in mode = %s" % runmode)
    while True: # Keep running even on false reply
        # Decide runmode (mostly for debug or should anything not work during presentations)
        if runmode == 1:
            recstring = record() 
        elif runmode == 2:
            recstring = c.magic
        elif runmode == 3:
            configureServo()

        # Compare string with the wanted string

        # Open door to predefined value if string is magic
        if recstring.lower() == c.magic.lower():
            print("Magic word recognized = %s" % c.magic)
            send("180") # actually 90 for the big Servo
            break

        # Open door to said digit
        elif recstring.isdigit():
            send(recstring)
            break

        # Exit if string is in exitWords
        elif recstring in c.exitWord:
            print("Exit word found - bye, bye")
            quit()
        receive(c.ClientKey) # Read esp serial debug
        ser.close()

if __name__ == '__main__':
    # This prevents execution on import
    main()