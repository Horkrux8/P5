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
    door.attach(0); // This is pin D3
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
            // If incomingString starts with Hostkey, strip HostKey of incoming to find degree
            int targetDegree = incomingString.substring(HostKey.length()).toInt();
            int changeDegree;

            Serial.println("CLIENT: Turning to: "+String(targetDegree));
            // Slow down rotation by rotating +1 degree every 10ms
            for (int currDegree=door.read(); currDegree!=targetDegree; currDegree += changeDegree) {
                changeDegree = (currDegree > targetDegree) ? -1 : 1; // Negate direction
                door.write(currDegree);
                delay(10);
            }
            Serial.println("CLIENT: done");
            Serial.println(ClientKey);
        }
    }
}