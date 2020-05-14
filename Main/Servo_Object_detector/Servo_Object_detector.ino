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
  while(Serial.available()>0)
  SerialData = Serial.readStringUntil(" ");
  Serial.println(SerialData);
  value = (SerialData).toInt();

  myservo.write(value);
  
  //delay(10);
}
