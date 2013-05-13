from get_wpilib import wpilib

import time

from utilities.kalman import Kalman
from robotmap import *

from utilities.pid import PIDDiffrence

class Drive(object):
	def __init__(self):
		"""
		Do things like create filters or initialize variables.
		"""
		# Create the kalman filters
		self.leftKalman = Kalman()
		self.rightKalman = Kalman()
		
		# Initialize PIDDiffrence for calculating error
		# in the wheels. That means that self.pidDiff.Get() will return the
		# value for the motor to get left-right to the setpoint
		self.pidDiff = PIDDiffrence(0.01, 0, 0, leftDriveEncoder, rightDriveEncoder)

		# Initialize variables for DriveForTime
		self.driveDistanceStarted = False

	def DriveTeleop(self):
		"""
		This is the method we will register as a task with the
		scheduler to be called in OperatorControl (ie. teleop)

		It is named "DriveTeleop" because when it is registered
		with the scheduler it uses that name to check if one is
		already registered if you tell it to. If it was just
		Teleop and we had a Teleop method from another class
		registered it would throw an error.
		"""

		# Update the kalman filters
		left = self.leftKalman.Update(joystick1.GetRawAxis(2)**3)
		right = self.rightKalman.Update(joystick1.GetRawAxis(5)**3)

		# Set the motors to the values
		robotDrive.TankDrive(left, right)

		# print("Left", left, "|", "Right", right)

		# We return false so this is never removed from the scheduler
		return False

	def Shift(self):
		# print("SHIFT CHECK")
		if joystick1.GetRawButton(11):
			shifters.Set(False)
			print("Shifted Up")
		elif joystick1.GetRawButton(10):
			shifters.Set(True)
			print("Shifted Down")

	def AutoShift(self, shift=False):
		if shift:
			# print("Shifted")
			pass # Shfit
		return True

	def DriveSpeed(self, speed=0.5):
		"""
		This will be able to be registered with the scheduler.

		Keyword arguments:
		@speed -- The speed to drive (default 0.5)
		"""

		robotDrive.TankDrive(speed, speed)
		return False
	
	def DriveDistance(self, distance, speed=0.5):
		"""
		This will be able to be registered with the scheduler
		and stop driving after after the distance is reached.
		
		Keyword arguments:
		@distance -- The distance to drive in encoder ticks
		@speed -- The speed to drive as a positive (default 0.5)
		"""
		if not self.driveDistanceStarted:
			self.driveDistanceStarted = True
			leftDriveEncoder.Reset()
			self.pidDiff.Reset()
			# Set encoders to be the same
			self.pidDiff.SetSetpoint(0.0)
			self.pidDiff.Enable()
			# Positive or negative speed
			self.direction = distance / abs(distance)
		
		# I believe we may need to subtract the diff from the right
		diff = self.pidDiff.Get()
		leftDriveEncoder.value+=.01
		print(diff)
		leftSpeed = speed*self.direction + diff
		rightSpeed = speed*self.direction
		
		
		


################### Register with scheduler ###################
from systems.scheduler import scheduler

drive = Drive()
scheduler.RegisterOperatorControlTask("Operator drive", drive.DriveTeleop)
scheduler.RegisterOperatorControlTask("Operator drive shift", drive.Shift)
