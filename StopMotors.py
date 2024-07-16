#!/usr/bin/python3

import sys
sys.path.append('/home/pi/MasterPi/')

import mecanum_ArcheoBot as mecanum

chassis = mecanum.MecanumChassis()

chassis.set_velocity(0, 0)

sys.exit(0)