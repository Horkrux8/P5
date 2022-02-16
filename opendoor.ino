// Library import
#include "Servo.h"

/* This program is going to wait for a serial message containing
the identity string, after that it is activating a servoengine */

String incomingString;
String HostKey;
String ClientKey;

// Setup
Servo door;
void setup(){
    door.attach(0);
    Serial.begin(9600);
    Serial.printf("\nCLIENT: Started \n");
    door.write(0); // Reset servo
}

void loop(){
    /* Read incoming serial lines as string and look for identifier
    if found change servo to found degree*/
    HostKey = "{IDENTIFIER-HOST}";
    ClientKey = "{IDENTIFIER-CLIENT}";

    if (Serial.available() > 0){
        // Read all incoming
        incomingString = Serial.readString();
        Serial.print("CLIENT: Found incoming serial: "+incomingString+"\n");

        if (incomingString.indexOf(HostKey) == 0){
            // If HostKey in incoming strip HostKey of incoming to find degree
            Serial.println(ClientKey);
            int degree = incomingString.substring(HostKey.length()).toInt();
            door.write(degree); 
        }
    }
}