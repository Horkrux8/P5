String incomingString;
String identityString = "{IDENTIFIER-HOST";
void setup(){
    Serial.begin(9600);
    Serial.printf("\nCLIENT: Started \n");
}
void loop(){
    if (Serial.available() > 0){
        incomingString = Serial.readString();
        Serial.print("CLIENT: Found incoming serial: "+incomingString+"\n");
        if (incomingString.indexOf("{IDENTIFIER-HOST}")){
            Serial.print("Recognized string");
        }
    }
}