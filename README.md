# P5 - "Tür der fetten Dame"

Dies ist eine Projektausarbeitung zum Bauen einer Sprachgesteuerten, automatischen Tür.

## Dokumentation der Arbeitspakete

### Material beschaffung

### Öffnungsmechanismus

### Software / Hardware

Die technische Umsetzung der Tür erfolgt mit zwei Geräten, einem Host (Laptop) und Client (Mikrocontronller / esp8266).
Der Host startet das Programm und dies erkennt was gesagt wird, wenn es das gesuchtet Wort is, wird der Client über das USB Kable benachrichtigt.
Der Client dursucht dan die empfangene Nachricht nach der Servo Konfiguration und stellt den Servo ein.

#### Genaueres - [talking.py](https://github.com/Horkrux8/P5/blob/main/talking.py)

Dies ist das Host Programm, es ist für Spracherkennung und benachrichtigungen an den Client verantwortlich.

Ich nutze eine Library (Klassen: `r.xyz()` & `m.xyz()`) welche in der lage ist eine Mikrofon aufnahme zu machen, und diese bei Erkennung von Ton stoppt.
```python
with m as source: r.adjust_for_ambient_noise(source) # Take ambient noise into account
    while True:
        print("Now Ready, listening in %s. (Press Ctrl+c to or say exit/quit/stop to quit)" % language_val)
        with m as source: audio = r.listen(source) # m is microphone (see configuration)
```

Die Aufnahme wird an eine Google API gechickt, welche dann den erkannten Satz zurück schickt.
```python
value = r.recognize_google(audio, language=language_val)
```
Danach wird `value` "decoded", also in normale Schrift umgewandelt.

In der funktion `opendoor(Degree)` wird die USB Verbindung (SerialCOM) konfiguriert und die Öffnungsweite an den ESP8266 geschickt.
```python
port, baud = [value for value in list(serialcom.values())] # Configuring serial
    ser = serial.Serial(port, baud, timeout=1)
    ser.write((HostKey+str(Degree)).encode())
```

#### Genaueres - [opendoor.ino](https://github.com/Horkrux8/P5/blob/main/opendoor.ino)

Dies ist das Client Programm, verantwortlich auf Benachrichtigungen zu empfangen und den Servo Motor anzusteuern.

Hier nutzen wir `Servo.h`, eine Library welche die Bedienung des Servos zu `Servo.write(1)`vereinfacht.


### Qualitätsprüfung

## Reflexion der Arbeitspakete

### Materialbeschaffung

### Öffnungsmechanismus

### Software / Hardware

### Qualitätsprüfung