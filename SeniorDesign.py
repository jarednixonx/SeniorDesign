from time import sleep
import picamera
import RPi.GPIO as GPIO
import cv2
import time
import signal
import sys
from threading import Timer

### LOCKS THE DOOR ###

def lockSolenoid():
	GPIO.output(solenoidPIN1,GPIO.HIGH)
	GPIO.output(solenoidPIN2, GPIO.HIGH)		

### UNLOCKS THE DOOR ###

def unlockSolenoid():
	GPIO.output(solenoidPIN1,GPIO.LOW)	
	GPIO.output(solenoidPIN2, GPIO.LOW)

### POWER OFF SOLENOID AFTER PROGRAM TERMINATION ###

def poweroff(signum, frame):
	unlockSolenoid()
	sys.exit(0)
	
### TURNS OFF AN LED PIN ###

def turnOff(pin):
	GPIO.output(pin,GPIO.HIGH)
	
### DRIVES RED LED ###

def redON():
	GPIO.output(redPIN,GPIO.LOW)
	GPIO.output(greenPIN,GPIO.HIGH)
	GPIO.output(bluePIN,GPIO.HIGH)
	
### DRIVES GREEN LED ###

def greenON():
	GPIO.output(redPIN,GPIO.HIGH)
	GPIO.output(greenPIN,GPIO.LOW)
	GPIO.output(bluePIN,GPIO.HIGH)

### DRIVES BLUE LED ###

def blueON():
	GPIO.output(redPIN,GPIO.HIGH)
	GPIO.output(greenPIN,GPIO.HIGH)
	GPIO.output(bluePIN,GPIO.LOW)

### FUNCTION TO LOCK THE DOOR BACK ###

def lockDoor():
	print("Time Up. Locking door")
	blueON()
	lockSolenoid()

### FUNCTION TO RESET STATE TO READY AFTER DENIAL ###

def denied():
	blueON()

### FACIAL RECOGNITION FUNCTION ###

def faceFind():
	imagePath = 'employeePhoto.jpg'
	cascPath = '/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml'

	faceCascade = cv2.CascadeClassifier(cascPath)

	image = cv2.imread(imagePath)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	faces = faceCascade.detectMultiScale(
		gray,
		scaleFactor = 1.1,
		minNeighbors = 4,
		minSize = (160,160),
		flags = cv2.cv.CV_HAAR_SCALE_IMAGE
		)

	if (len(faces) == 1):
		print("numer of faces is:", len(faces))
		print('Access Granted!')
		greenON()
		unlockSolenoid()
		
		t = Timer(10.0,lockDoor)
		t.start()

	elif (len(faces) > 1):
		print("numer of faces is:", len(faces))
		print('Access Denied, 1 face at a time, please')
		redON()

		t = Timer(6.0,denied)
		t.start()
	else:
		print('Access Denied, no faces found')
		redON()

		t = Timer(6.0,denied)
		t.start()

	print "Found {0} faces!".format(len(faces))

	for(x, y, w, h) in faces:
		cv2.rectangle(image, (x,y), (x+w, y+h), (0, 255, 0), 2)

	#cv2.imshow("Faces found", image)
	#cv2.waitKey(10000)
	#cv2.destroyAllWindows()
	#cv2.waitKey(1)

	return

### MAIN FUNCTION HERE ###

bluePIN = 5
greenPIN = 6
redPIN = 13

solenoidPIN1 = 26
solenoidPIN2 = 19

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(redPIN,GPIO.OUT)
GPIO.setup(greenPIN,GPIO.OUT)
GPIO.setup(bluePIN,GPIO.OUT)

GPIO.setup(solenoidPIN1,GPIO.OUT)
GPIO.setup(solenoidPIN2, GPIO.OUT)

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

turnOff(redPIN)
turnOff(greenPIN)
turnOff(bluePIN)

blueON()

unlockSolenoid()

camera = picamera.PiCamera()

print('Press the button for rack access.')

signal.signal((signal.SIGINT | signal.SIGTERM), poweroff)
#signal.pause()

while True:
	input_state = GPIO.input(18)

	if input_state == False:
		print('Photo taken... Please Wait.')
		camera.capture('employeePhoto.jpg')

		# Call function to detect faces.
		faceFind()

		sleep(0.2)

		print('Press the button for rack access.')
		
