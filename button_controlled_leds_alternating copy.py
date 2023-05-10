from time import sleep
import threading
import RPi.GPIO as GPIO    # Import GPIO Library 
GPIO.setmode(GPIO.BOARD)   # Use Physical Pin Numbering Scheme
button1=16                 # Button 1 is connected to physical pin 16
button2=12                 # Button 2 is connected to physical pin 12
LED1=22                    # LED 1 is connected to physical pin 22
LED2=18                    # LED 2 is connected to physical pin 18
BS1=False                  # Set Flag BS1 to indicate LED is initially off
BS2=False                  # Set Flag BS2 to indicate LED is initially off
BlinkRate = .2

def setup():
    GPIO.setup(button1,GPIO.IN,pull_up_down=GPIO.PUD_UP) # Make button1 an input, Activate Pull UP Resistor
    GPIO.setup(button2,GPIO.IN,pull_up_down=GPIO.PUD_UP) # Make button 2 an input, Activate Pull Up Resistor
    GPIO.setup(LED1,GPIO.OUT,) # Make LED 1 an Output
    GPIO.setup(LED2,GPIO.OUT)  # Make LED 2 an Output

# flashing thread
def thread_function():
    global BS1
    global BlinkRate
    while(1):
        while BS1 == True:
            GPIO.output(LED2,False)
            GPIO.output(LED1,True)
            sleep(BlinkRate)
            GPIO.output(LED1,False)
            GPIO.output(LED2,True)
            sleep(BlinkRate) 
        GPIO.output(LED2,False)
        GPIO.output(LED1,False)     

def destroy():
    GPIO.output(LED1,False)
    GPIO.output(LED2,False)
    GPIO.cleanup()

def main():
    global BS1
    global BS2
    global BlinkRate
    x = threading.Thread(target=thread_function, args=(), daemon=True)  
    x.start() 
   
    while(1):                  
        if GPIO.input(button1)==0:   
            GPIO.output(LED1,False)
            GPIO.output(LED2,False)          
            print ("Button 1 Was Pressed")
            if BS1==False:               
                BS1=True     
            else:                         
                BS1=False
            sleep(.2)  
        if GPIO.input(button2)==0:
            print ("Button 2 Was Pressed")
            if BlinkRate < .051:
                BlinkRate = .2
            else:
                BlinkRate -= .1
            print (BlinkRate)
            sleep(.2)


if __name__ == "__main__":    
    setup()
    try:
        main()       
    except KeyboardInterrupt:
        destroy()    
                       
        