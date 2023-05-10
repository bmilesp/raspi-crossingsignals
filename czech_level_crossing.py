from time import sleep
from gpiozero import Servo
import threading
import RPi.GPIO as GPIO    # Import GPIO Library 
GPIO.setmode(GPIO.BOARD)   # Use Physical Pin Numbering Scheme
button1=16                 # Button 1 is connected to physical pin 16
button2=12
button3=13                 # Button 2 is connected to physical pin 12
LED1=22                    # LED 1 is connected to physical pin 22
LED2=18
LED3=15      
servoGPIO=17              # gpio 17 IS PIN 11
BS1=False                  # Set Flag BS1 to indicate LED is initially off
BS2=False
BS3=False                  # Set Flag BS2 to indicate LED is initially off
BlinkRate = .2
SecondaryBlinkRate = .5
ButtonTactileSleep = .2
ThreadLoopThrottle = .01
primaryServo="" # var for PWM servo setup
SERVOmaxPW=2.9/1000
SERVOminPW=0/1000
maxServoTicks = 70
ArmDown = False

def setup():
    global primaryServo
    GPIO.setup(button1,GPIO.IN,pull_up_down=GPIO.PUD_UP) # Make button1 an input, Activate Pull UP Resistor
    GPIO.setup(button2,GPIO.IN,pull_up_down=GPIO.PUD_UP) # Make button 2 an input, Activate Pull Up Resistor
    GPIO.setup(button3,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(LED1,GPIO.OUT,) # Make LED 1 an Output
    GPIO.setup(LED2,GPIO.OUT)  # Make LED 2 an Output
    GPIO.setup(LED3,GPIO.OUT)
    primaryServo = Servo(servoGPIO,min_pulse_width=SERVOminPW,max_pulse_width=SERVOmaxPW)

# flashing thread
def primary_lights():
    global BS1
    global BlinkRate
    while(1):
        sleep(ThreadLoopThrottle)
        while BS1 == True:
            GPIO.output(LED2,False)
            GPIO.output(LED1,True)
            sleep(BlinkRate)
            GPIO.output(LED1,False)
            GPIO.output(LED2,True)
            sleep(BlinkRate) 
        GPIO.output(LED2,False)
        GPIO.output(LED1,False)

def secondary_light():
    global BS3
    while(1):
        sleep(ThreadLoopThrottle)
        while BS3 == True:
            GPIO.output(LED3,True)
            sleep(SecondaryBlinkRate)
            GPIO.output(LED3,False)
            sleep(SecondaryBlinkRate) 
        GPIO.output(LED3,False)     

def servoDown():
    sleep(1)
    for value in range(0,maxServoTicks):
        value2=(float(value))/100
        primaryServo.value=value2
        sleep(.1)

def servoUp():
    for value in range(0,maxServoTicks):
        value2=(maxServoTicks - float(value))/100
        primaryServo.value=value2
        sleep(.1)
        print(value)
        print(value2)

def destroy():
    GPIO.output(LED1,False)
    GPIO.output(LED2,False)
    GPIO.output(LED3,False)
    GPIO.output(Servo,False)
    primaryServo.stop()
    GPIO.cleanup()

def main():
    global BS1
    global BS2
    global BS3
    global BlinkRate
    global ArmDown

    BS3=True
    primary_light_thread = threading.Thread(target=primary_lights, args=(), daemon=True)  
    secondary_light_thread = threading.Thread(target=secondary_light, args=(), daemon=True) 
    #servo_thread = threading.Thread(target=servo, args=(), daemon=True) 
    #servo_thread.start()
    primary_light_thread.start() 
    secondary_light_thread.start() 
   
    while(1):                  
        if GPIO.input(button1)==0:   
            GPIO.output(LED1,False)
            GPIO.output(LED2,False)          
            print ("Button 1 Was Pressed")
            if BS1==False: 
                BS3=False              
                BS1=True 
                ArmDown = True
                servoDown() 
            else:
                servoUp()
                sleep(1)                         
                BS1=False
                BS3=True
                sleep(30)
                BS3=False
            sleep(ButtonTactileSleep)  
        if GPIO.input(button2)==0:
            print ("Button 2 Was Pressed")
            if BlinkRate < .051:
                BlinkRate = .2
            else:
                BlinkRate -= .1
            print (BlinkRate)
            sleep(ButtonTactileSleep)
        if GPIO.input(button3)==0:
            print ("Button 3 Was Pressed")
            GPIO.output(LED3,False)     
            if BS3==False:               
                BS3=True     
            else:                         
                BS3=False
            sleep(ButtonTactileSleep)


if __name__ == "__main__":    
    setup()
    try:
        main()       
    except KeyboardInterrupt:
        destroy()    
                       
        