#include <Servo.h>

Servo myservo;
String SerialData; 
int value;

int pin = 9;  

void setup() 
{
  pinMode(9, OUTPUT);
  myservo.attach(9); 
  Serial.begin(9600); 
  Serial.setTimeout(3);
}

void loop() 
{
  while(Serial.available()>0)
  {
    SerialData = Serial.readString();
    Serial.println(SerialData);
    value = (SerialData).toInt();

    myservo.write(value);
  }

}
