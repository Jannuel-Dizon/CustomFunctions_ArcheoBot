#!/usr/bin/python3
# coding=utf8
import sys
sys.path.append('/home/pi/MasterPi/')
import math
import threading
import HiwonderSDK.Board as Board

class MecanumChassis:
    # A = 67  # mm
    # B = 59  # mm
    # WHEEL_DIAMETER = 65  # mm

    def __init__(self, a=67, b=59, wheel_diameter=65):
        self.a = a
        self.b = b
        self.wheel_diameter = wheel_diameter
        self.velocity = 0
        self.angular_rate = 0

    def reset_motors(self):
        for i in range(1, 5):
            Board.setMotor(i, 0)
            
        self.velocity = 0
        self.angular_rate = 0

    # def set_velocity(self, velocity, direction, angular_rate, fake=False):
    # Max speed of -100 to 100 mm/s
    def set_velocity(self, velocity, angular_rate, fake=False):
        """
        Use polar coordinates to control moving
        motor1 v1|  ↑  |v2 motor2
                 |     |
        motor3 v3|     |v4 motor4
        :param velocity: mm/s
        :param angular_rate:  The speed at which the chassis rotates
        :param fake:
        :return:
        """

        vp = -angular_rate * (self.a + self.b)
        vl = int(velocity - vp) 
        vr = int(velocity + vp)

        if fake:
            return
        Board.setMotor(1, vl) 
        Board.setMotor(2, vr)
        Board.setMotor(3, vl)
        Board.setMotor(4, vr)
        self.velocity = velocity
        self.angular_rate = angular_rate