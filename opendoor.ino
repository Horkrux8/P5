// Library import
#include "Servo.h"

/* This program is going to wait for a serial message containing
the identity string, after that it is activating a servoengine */

String incomingString;
String HostKey;
String ClientKey;
String TargetKey;
String ChangeKey;

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
            // If incomingString starts with Hostkey, strip HostKey of incoming to find target & change rate
            int targetDegree = incomingString.substring(HostKey.length()).toInt();
            int changeDegree = 4;
            int currDegree = door.read();
            int overflowDegree = (currDegree - targetDegree) % changeDegree;
            changeDegree = (currDegree > targetDegree) ? changeDegree*-1 : changeDegree*1; // Negate direction
            Serial.printf("CLIENT: Starting from: %d, target: %d, at rate: %d\n", currDegree, targetDegree, changeDegree);
            
            if (overflowDegree != 0){
                door.write(currDegree + overflowDegree);
                Serial.printf("Adjusting to step size: %d, starting from %d\n", changeDegree, currDegree - overflowDegree);
                currDegree = currDegree + overflowDegree;
            }

            // Slow down rotation by rotation +1 degree every 10ms
            for (currDegree; currDegree!=targetDegree; currDegree += changeDegree) {
                Serial.printf("CLIENT: Turning to: %d, target: %d, step size: %d \n", currDegree, targetDegree, changeDegree);
                door.write(currDegree);
                delay(10);
            }

            door.write(targetDegree); // Close any remaining gap to target
            Serial.printf("CLIENT: done (at: %d) \n", door.read());
            Serial.println(ClientKey);
            // Everything beyond ClientKey wont be readed by Host
        }
    }
}