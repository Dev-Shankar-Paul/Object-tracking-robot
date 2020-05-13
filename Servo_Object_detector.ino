#include <Servo.h>

Servo myservo;
String SerialData; 
int value = 0;

int pin = 9;   

void setup() {
  pinMode(9, OUTPUT);
  myservo.attach(9); 
  Serial.begin(9600); 
}

void loop() {
  if(Serial.available()>0)
  SerialData = Serial.readStringUntil("\n");

  value = (SerialData).toInt();

  myservo.write(value);
  
  //delay(10);
}
