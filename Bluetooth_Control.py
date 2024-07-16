#!/usr/bin/python3
# coding=utf8
import sys
sys.path.append('/home/pi/MasterPi/')
import cv2
import time
import threading
import signal
import yaml_handle
import numpy as np
import pygame
# from ultralytics import YOLO
"""
FOr using Raspberry Camera
from picamera.array import PiRGBArray
from picamera import PiCamera
"""
import mecanum_ArcheoBot as mecanum


if sys.version_info.major == 2:
	print('Please run this program with python3!')
	sys.exit(0)
"""
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(320, 240))
"""
chassis = mecanum.MecanumChassis()
# model = YOLO('YOLO_Model\shellsv4.pt')
pygame.init()

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
for joystick in joysticks:
	joystick.init()
	# name = joystick.get_name()
	# print(name)

lab_data = None
def load_config():
	global lab_data, servo_data

	lab_data = yaml_handle.get_yaml_data(yaml_handle.lab_file_path)

def initMove():
	chassis.set_velocity(0,1)
	time.sleep(5)
	chassis.set_velocity(0,-1)
	time.sleep(5)
	chassis.set_velocity(100,0)
	time.sleep(5)

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
	initMove()

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
	chassis.set_velocity(0, 0)
	print("Bluetooth Control Exit")
	sys.exit(0)


def move():
	global _stop
	global __isRunning
	global joystick

	while True:
		# print("__isRunning: ", __isRunning)
		if __isRunning:
			i = 0
			for event in pygame.event.get():
				i = i + 1
			# print(event)
			# if event.type == pygame.JOYAXISMOTION:
			# print(event.type)
			# Change 0 or 4 depending on the controller i guess
			x_speed = pygame.joystick.Joystick(0).get_axis(0)
			y_speed = pygame.joystick.Joystick(0).get_axis(1)
			if not abs(x_speed) > 0.05:
				x_speed = 0

			if abs(y_speed) > 0.05:
				y_speed = -(100 * y_speed)
			else:
				y_speed = 0

			print("y_speed: ", y_speed)
			print("x_speed: ", x_speed)
			chassis.set_velocity(y_speed, x_speed)
			time.sleep(0.5)
		else :
			print("_stop: ", _stop)
			if _stop:
				print('ok')
				_stop = False
				chassis.set_velocity(0,0)
				time.sleep(1.5)
			break

# Run the subthread
# th = threading.Thread(target=move)
# th.setDaemon(True)

def run(img):
	global __isRunning
	 
	if not __isRunning:  # Detect whether the game is started, if not, return the original image.
		return img
	else:
		# result = model.predict(img, conf=0.5)
		# annotated_frame = result[0].plot()
		return annotated_frame

if __name__ == '__main__':
	# Initialize the robot
	init()
	start()

	# Set-up Handler to stop running thread
	signal.signal(signal.SIGINT, exit)

	# Start the thread
	th = threading.Thread(target=move)
	th.setDaemon(True)
	th.start()

	# Video capture from usb cam
	cap = cv2.VideoCapture('http://127.0.0.1:8080?action=stream')
	while True:
		ret,img = cap.read()
		if ret:
			frame = img.copy()
			# Frame = run(frame)  
			# frame_resize = cv2.resize(Frame, (320, 240))
			# cv2.imshow('frame', frame_resize)
			key = cv2.waitKey(1)
		if key == 27:
			break
		else:
			time.sleep(0.01)
		"""
		For Raspberry camera
		for img in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
			# grab the raw NumPy array representing the image, then initialize the timestamp
			# and occupied/unoccupied text
			frame = img.array
			Frame = run(frame)
			frame_resize = cv2.resize(Frame, (320, 240))
			cv2.imshow('frame', frame_resize)
			key = cv2.waitKey(1)
			rawCapture.truncate(0)
			if key == 27:
				break
		"""

	cap.release()
	cv2.destroyAllWindows()
	th.join

