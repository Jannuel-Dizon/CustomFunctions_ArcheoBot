#!/usr/bin/python3
# coding=utf8
import sys
sys.path.append('/home/pi/MasterPi/')
import os
print("DISPLAY:", os.environ['DISPLAY'])
import cv2
import time
import threading
import signal
import yaml_handle
from picamera.array import PiRGBArray
from picamera import PiCamera
# import mecanum_ArcheoBot as mecanum


if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(320, 240))

# chassis = mecanum.MecanumChassis()

lab_data = None
def load_config():
    global lab_data, servo_data
    
    lab_data = yaml_handle.get_yaml_data(yaml_handle.lab_file_path)

# def initMove():
# 	chassis.set_velocity(0,0.5)
# 	time.sleep(1)
# 	chassis.set_velocity(0,-0.5)
# 	time.sleep(1)

# set buzzer 
def setBuzzer(timer):
    Board.setBuzzer(0)
    Board.setBuzzer(1)
    time.sleep(timer)
    Board.setBuzzer(0)

_stop = False
__isRunning = False

# Reset variable
def reset(): 
    global _stop

    _stop = False

# APP initialized calling
def init():
    print("Bluetooth Control Init")
    load_config()
    # initMove()

# APP starts game calling
def start():
    global __isRunning
    reset()
    __isRunning = True
    print("Bluetooth Control Start")

# APP stops game calling
def stop():
    global _stop
    global __isRunning
    _stop = True
    __isRunning = False
    print("Bluetooth Control Stop")

# APP exits game calling
def exit():
    global _stop
    global __isRunning
    _stop = True
    __isRunning = False
    print("Bluetooth Control Exit")


# def move():
# 	global _stop
# 	global __isRunning

# 	while True:
# 		if __isRunning:
# 			chassis.set_velocity(50,0)
# 			time.sleep(1)
# 		else :
# 			if _stop:
# 				print('ok')
# 				_stop = False
# 				chassis.set_velocity(0,0)
# 				time.sleep(1.5)               
# 			time.sleep(0.01)

# Run the subthread
# th = threading.Thread(target=move)
# th.setDaemon(True)
# th.start()

def run(img):
    global __isRunning
     
    if not __isRunning:  # Detect whether the game is started, if not, return the original image.
        return img
    else:
        return img

if __name__ == '__main__':
	init()
	start()
	while True:
		for img in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
			# grab the raw NumPy array representing the image, then initialize the timestamp
			# and occupied/unoccupied text
			frame = img.array
			Frame = run(frame)
			frame_resize = cv2.resize(Frame, (320, 240))
			cv2.imshow('frame', frame_resize)
			key = cv2.waitKey(1)
			if key == 27:
				break
	cv2.destroyAllWindows()

