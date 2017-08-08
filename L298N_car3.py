import RPi.GPIO as GPIO
import time

#GPIO
INT1 = 15
INT2 = 16
INT3 = 13
INT4 = 12

def init():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(INT1,GPIO.OUT)
	GPIO.setup(INT2,GPIO.OUT)
	GPIO.setup(INT3,GPIO.OUT)
	GPIO.setup(INT4,GPIO.OUT)

def go(seconds):
	init()
	GPIO.output(INT1,GPIO.HIGH)
	GPIO.output(INT2,GPIO.LOW)
	GPIO.output(INT3,GPIO.LOW)
	GPIO.output(INT4,GPIO.HIGH)
	stop(seconds);

def back(seconds):
	init()
	GPIO.output(INT1,GPIO.LOW)
	GPIO.output(INT2,GPIO.HIGH)
	GPIO.output(INT3,GPIO.HIGH)
	GPIO.output(INT4,GPIO.LOW)
	stop(seconds);

def left(seconds):
	init()
	GPIO.output(INT1,GPIO.HIGH)
	GPIO.output(INT2,GPIO.LOW)
	GPIO.output(INT3,False)
	GPIO.output(INT4,False)
	stop(seconds);

def right(seconds):
	init()
	GPIO.output(INT1,GPIO.LOW)
	GPIO.output(INT2,GPIO.HIGH)
	GPIO.output(INT3,False)
	GPIO.output(INT4,False)
	stop(seconds);

def stop(seconds):
	time.sleep(seconds)
	GPIO.cleanup()

if __name__ == "__main__":
	back(2)
	go(2)
	right(2)
	right(2)
	go(2)

