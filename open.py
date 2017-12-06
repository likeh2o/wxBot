import RPi.GPIO as GPIO
import time

#GPIO
INT1 = 7

def init():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(INT1,GPIO.OUT)

def open(seconds):
	init()
	GPIO.output(INT1,GPIO.HIGH)
	stop(seconds);

def stop(seconds):
	time.sleep(seconds)
	GPIO.cleanup()

if __name__ == "__main__":
	open(1)

