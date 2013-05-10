from get_wpilib import wpilib

from drive import drive

class Test(object):
	def testing(self):
		"""
		Print to the console.
		"""
		# print("Testing")
		return False

################### Register with scheduler ################### 
# from scheduler import scheduler

testing = Test()
# scheduler.RegisterOperatorControlTask("Testing", testing.testing)