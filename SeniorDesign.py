from time import sleep
import picamera
import RPi.GPIO as GPIO
import cv2
import time
from threading import Timer

# FUNCTION DEFINITION FOR FACEFIND


def moveSolenoid():
	GPIO.output(solenoidPIN,GPIO.LOW)		
#	print('solenoid moving: ')	comment this back in while testing solenoid -eledui

def stopSolenoid():
	GPIO.output(solenoidPIN,GPIO.HIGH)	
	print('solenoid stop: ')

	
def turnOff(pin):
	GPIO.output(pin,GPIO.HIGH)
	

def redON():
	GPIO.output(redPIN,GPIO.LOW)
	GPIO.output(greenPIN,GPIO.HIGH)
	GPIO.output(bluePIN,GPIO.HIGH)
	

def greenON():
	GPIO.output(redPIN,GPIO.HIGH)
	GPIO.output(greenPIN,GPIO.LOW)
	GPIO.output(bluePIN,GPIO.HIGH)

def blueON():
	GPIO.output(redPIN,GPIO.HIGH)
	GPIO.output(greenPIN,GPIO.HIGH)
	GPIO.output(bluePIN,GPIO.LOW)


def lockDoor():
	print("Time Up. Locking door")
	blueON()

def denied():
	blueON()


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
		
		t = Timer(10.0,lockDoor)
		t.start()

	elif (len(faces) > 1):
		print("numer of faces is:", len(faces))
		print('Access Denied, 1 face at a time, please')
		redON()
		t = Timer(3.0,denied)
		t.start()
	else:
		print('Access Denied, no faces found')
		redON()
		t = Timer(3.0,denied)
		t.start()

	print "Found {0} faces!".format(len(faces))

	for(x, y, w, h) in faces:
		cv2.rectangle(image, (x,y), (x+w, y+h), (0, 255, 0), 2)


#	time.sleep(10)
	#lockDoor()
#!!!!!!! NOTE: Keeping functions below for testing purposes.!!!!!!
	cv2.imshow("Faces found", image)
	cv2.waitKey(10000)
	cv2.destroyAllWindows()
	cv2.waitKey(1)
	


	return

# START THE MAIN FUNCTION HERE

GPIO.cleanup()

bluePIN = 5
greenPIN = 6
redPIN = 13


solenoidPIN = 26


GPIO.setmode(GPIO.BCM)
GPIO.setup(redPIN,GPIO.OUT)
GPIO.setup(greenPIN,GPIO.OUT)
GPIO.setup(bluePIN,GPIO.OUT)

GPIO.setup(solenoidPIN,GPIO.OUT)

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(18, GPIO.IN)

turnOff(redPIN)
turnOff(greenPIN)
turnOff(bluePIN)



blueON()

camera = picamera.PiCamera()

print('Press the button for rack access.')

while True:
	
	input_state = GPIO.input(18)




	moveSolenoid()
#	sleep(2)
#	stopSolenoid()

	if input_state == False:
		print('Photo taken... Please Wait.')
		camera.capture('employeePhoto.jpg')

		# Call function to detect faces.
		faceFind()

		sleep(0.2)
		#GPIO.cleanup()
		print('Press the button for rack access.')

'''
	blueON()
	sleep(3)
	turnOff(bluePIN)
	sleep(0.5)


	redON()
	sleep(3)
	turnOff(redPIN)
	sleep(0.5)


	greenON()
	sleep(3)
	turnOff(greenPIN)
	sleep(0.5)
'''
