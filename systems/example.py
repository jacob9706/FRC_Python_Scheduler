from get_wpilib import wpilib

from robotmap import *


class ClassName(object):

	def __init__(self):
		"""
		Do things like create filters or initialize variables.
		"""
		pass

	def ClassNameTeleop(self):
		"""
		This is the method we will register as a task with the 
		scheduler to be called in OperatorControl (ie. teleop)

		Convention is to name it "ClassNameTeleop" because when 
		it is registered with the scheduler it uses that name 
		to check if one is already registered if you tell it to. 
		If it was just Teleop and we had a Teleop method from 
		another class registered it would not schedule it.
		"""
		pass


################### Register with scheduler ###################
from systems.scheduler import scheduler

className = ClassName()
scheduler.RegisterOperatorControlTask("ClassName Teleop", className.ClassNameTeleop)