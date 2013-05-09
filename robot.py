# To test open a terminal and navigate to fake-wpilib
# then run ./test.sh import_test --robot-path ..

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


from get_wpilib import wpilib

# Import the robot map to be able to access things like
# joystics added at the bottom of robotmap.py
from robotmap import joystick1

# Import the instance of Scheduler called scheduler to be 
# able to use it.
from scheduler import scheduler

# Import the drive wich also registers the operator
# control task.
import drive

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
			scheduler.Autonomous(debug = False)

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
		if joystick1.GetRawButton(1):
			raise RuntimeError("\n========== Restarting Robot ==========")


	def RegisterAutonomous(self):
		scheduler.RegisterAutonomousTask(# The name to print for debugging
										 "Drive for one second at half speed", 
										 # The task to add (function or method)
										 drive.drive.DriveForTime, 
										 # The type of task
										 scheduler.SEQUENTIAL_TASK,
										 # The parameters for the task.
										 # These are unique to the task added
										 1000, # Time to run
										 0.5) # Speed to run at


def run():
	robot = MyRobot()
	robot.StartCompetition()
	return robot