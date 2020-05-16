# Object-tracking-robot
This is my ISOC (IEEE Summer of Code) Project. 

## Aim : To create an object tracking robot using a Raspberry-Pi

Due to the lockdown, parts are currently unavailable, so, in order to make do with the products in my possession right now, I tried to control a servo instead. If the object moves to the left of the screen, the servo does so as well and vice versa.

The Main folder contains the important code whereas the Reference folder contains some residual code which is more detailed than the master code. Master.py contains the final code. 

## Working :
First we need to set the colour of the object we have to detect. We can do so by adjusting the trackbar sliders. Once that is done, make sure your Arduino is connected (along with a servo) and that the code is uploaded to it. Then press 'q' on your keyboard. 

As you move the object, the servo should move along with it as well. 

## Libraries used :
### In python - 
1) cv2 (opencv-python)
2) math 
3) serial
4) sys
### In Arduino - 
1) Servo

## Future plans :
In the near future, I plan to replace the Arduino-Servo system for a Raspberry-pi and create a fully working Object Tracking Robot. 


