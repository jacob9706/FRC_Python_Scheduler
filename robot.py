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

# Do both so we don't have to refer to tilt.tilt and were
# also have access to constants
from systems.tilt import tilt

from utilities import wait

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
		scheduler.ListAutonomousTasks()

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
		# These run the whole time to spin the wheel and make sure the tilt 
		# statys at the right position
		scheduler.RegisterAutonomousTask("ShooterContinuous", shooter.ShooterContinuous, scheduler.PARALLEL_TASK)
		scheduler.RegisterAutonomousTask("TiltContinuous", tilt.TiltContinuous, scheduler.PARALLEL_TASK)
		
		# Spin up wheel, tilt and wait 3 seconds for it to reach speed		
		scheduler.RegisterAutonomousTask("Set Shooter Speed 0.5", shooter.SetSpeed, scheduler.PARALLEL_TASK, shooter.SHOOTER_INFIELD)
		scheduler.RegisterAutonomousTask("Tilt", tilt.TiltToValue, scheduler.PARALLEL_TASK, tilt.TILT_PYRIMID_SIDE_PRACTICE)
		
		# The wait.Wait() is just an enpty function. The scheduler just waits
		# for the registered empty task to timeout
		scheduler.RegisterAutonomousTimedTask("Wait 3 Seconds", wait.Wait, 3.0)
		
		# Add 3 sequential shots
		scheduler.RegisterAutonomousTask("Shoot And Load1", shooter.ShootAndLoad)
		scheduler.RegisterAutonomousTask("Shoot And Load2", shooter.ShootAndLoad)
		scheduler.RegisterAutonomousTask("Shoot And Load3", shooter.ShootAndLoad)
		
		# Tilt back down and put wheel in powersaver mode
		scheduler.RegisterAutonomousTask("SHOOTER POWER SAVING MODE", shooter.SetSpeed, scheduler.PARALLEL_TASK, shooter.SHOOTER_POWER_SAVING_MODE)
		scheduler.RegisterAutonomousTask("Tilt", tilt.TiltToValue, scheduler.PARALLEL_TASK, tilt.TILT_PYRIMID_SIDE_PRACTICE)
		

def run():
	"""
	The entrypoint for the robot.

	We return the robot instance for the fake-wpilib testing.
	"""
	robot = MyRobot()
	robot.StartCompetition()
	return robot
