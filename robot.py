# To test open a terminal and navigate to fake-wpilib
# then run "./test.sh import_test --robot-path .."

# Count source files in current dir "cat *.c | wc -l"

# You may notice that no OperatorControl tasks have been
# added in this file. This is because they have been added
# within their moduals. For example in the drive.py file
# we have the class definition then under that we have an
# import for the scheduler object declared at the bottom
# of the scheduler.py file. Under the import we register
# the Drive.DriveTeleop() with the scheduler. This allows 
# for us to keep the robot.py file pretty clean. for an
# operator control task to registered you just have to
# include the modual


# Import the wpilib, if it is not avaliable it will import 
# fake wpilib
from get_wpilib import wpilib

# Import the robot map to be able to access things like
# joystics added at the bottom of robotmap.py
from robotmap import *

# Import the instance of Scheduler called scheduler to be 
# able to use it.
from systems.scheduler import scheduler

# Import the modules wich also registers the operator
# control tasks.
from systems.drive import drive
from systems.collector import collector
from systems.shooter import shooter
from systems.tilt import tilt

class MyRobot(wpilib.SimpleRobot):

	def __init__(self):
		super().__init__()
		print("\n========== Robot Initialized ==========")


	def Disabled(self):
		print("\n========== Disabled Initialized ==========")

		while self.IsDisabled():
			# Check if we should reload the code
			self.CheckRestart()
			
			# Wait so cpu is not running at 100%
			wpilib.Wait(0.01)


	def Autonomous(self):
		print("\n========== Autonomous Initialized ==========")

		# Get an configure the watchdog
		dog = self.GetWatchdog()
		dog.SetEnabled(True)
		dog.SetExpiration(1.0)

		# The reason we register the autonomous each time is because
		# when it is done and all have resolved it is cleared
		self.RegisterAutonomous()

		while self.IsAutonomous() and self.IsEnabled():
			# Feed the watchdog
			dog.Feed()

			# Run the scheduled autonomous tasks while in enabled autonomous
			scheduler.Autonomous(debug = True)

			# Wait so cpu is not running at 100%
			wpilib.Wait(0.01)

		# We clear the tasks just incase they all did not resolve
		# that way next time autonomous is run it will not be adding
		# registries ontop of the non resolved ones
		scheduler.ClearAutonomousTasks()


	def OperatorControl(self):
		print("\n========== OperatorControl Initialized ==========")

		# Get an configure the watchdog
		dog = self.GetWatchdog()
		dog.SetEnabled(True)
		dog.SetExpiration(0.25)

		while self.IsOperatorControl() and self.IsEnabled():
			# Feed the watchdog
			dog.Feed()

			# Run the scheduled operator control tasks while enabled
			scheduler.OperatorControl(debug = False)

			# Wait so cpu is not running at 100%
			wpilib.Wait(0.01)


	def CheckRestart(self):
		"""
		Reload the code by raising an exception. There will be about 
		a 5 second delay then you will be good to go.
		"""
		if joystick1.GetRawButton(1):
			raise RuntimeError("\n========== Restarting Robot ==========")


	def RegisterAutonomous(self):
		"""
		Register the autonomous tasks.
		"""

		scheduler.RegisterAutonomousTask("Shift", drive.AutoShift, scheduler.PARALLEL_TASK, True)

		scheduler.RegisterAutonomousTimedTask(# The name to print for debugging
										 "Drive for seven seconds at half speed", 
										 # The task to add (function or method)
										 drive.DriveSpeed,
										 # Time to run
										 7,
										 # The type of task
										 scheduler.SEQUENTIAL_TASK,
										 # The parameters for the task.
										 # These are unique to the task added
										 0.5) # Speed to run at


def run():
	"""
	The entrypoint for the robot.

	We return the robot instance for the fake-wpilib testing.
	"""
	robot = MyRobot()
	robot.StartCompetition()
	return robot
