from get_wpilib import wpilib

from robotmap import *


class Collector(object):

	def __init__(self):
		"""
		Do things like create filters or initialize variables.
		"""
		self.canRun = True

	def CollectorTeleop(self):
		"""
		This is the method we will register as a task with the 
		scheduler to be called in OperatorControl (ie. teleop)

		Convention is to name it "ClassNameTeleop" because when 
		it is registered with the scheduler it uses that name 
		to check if one is already registered if you tell it to. 
		If it was just Teleop and we had a Teleop method from 
		another class registered it would not schedule it.
		"""
		
		# If the left or right bumper is pressed
		if (joystick1.GetRawButton(5) or joystick1.GetRawButton(6)) and self.canRun:
			lowerCollectorMotor.Set(-1.0)
			upperCollectorMotor.Set(1.0)
			print("Running Collector")
		else:
			lowerCollectorMotor.Disable()
			upperCollectorMotor.Disable()


################### Register with scheduler ###################
from systems.scheduler import scheduler

collector = Collector()
scheduler.RegisterOperatorControlTask("Collector Teleop", collector.CollectorTeleop)