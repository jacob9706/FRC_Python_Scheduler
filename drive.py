from get_wpilib import wpilib

import time

from kalman import Kalman
from robotmap import *

class Drive(object):
	def __init__(self):
		"""
		Fetch all the required objects for the system and do 
		things like create filters or initialize variables.
		"""
		# Create the kalman filters
		self.leftKalman = Kalman()
		self.rightKalman = Kalman()

		# Initialize variables for DriveForTime
		self.time = 0

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
		left = self.leftKalman.Update(joystick1.GetRawAxis(1)**3)
		right = self.rightKalman.Update(joystick1.GetRawAxis(4)**3)

		# Set the motors to the values
		leftDriveMotor.Set(left)
		rightDriveMotor.Set(right)
		
		print("Left", left, "|", "Right", right)

		# We return false so this is never removed from the scheduler
		return False

	def Shift(self):
		# print("SHIFT CHECK")
		if joystick1.GetRawButton(2):
			pass # Shift here

	def AutoShift(self, shift=False):
		if shift:
			# print("Shifted")
			pass # Shfit
		return True

	def DriveSpeed(self, speed=0.5):
		"""
		This will be able to be registered with the scheduler
		and stop driving after X amount of time.

		The reason we default time to 0 is just in case the 
		method is registered with the scheduler without any
		parameters.

		Keyword arguments:
		@time -- The time to do this is milliseconds
		"""


		leftDriveMotor.Set(speed)
		rightDriveMotor.Set(speed)
		return False



################### Register with scheduler ###################
from scheduler import scheduler

drive = Drive()
scheduler.RegisterOperatorControlTask("Operator drive", drive.DriveTeleop)
scheduler.RegisterOperatorControlTask("Operator drive shift", drive.Shift)