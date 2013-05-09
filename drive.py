import wpilib, time

from kalman import Kalman
from robotmap import leftDriveMotor, rightDriveMotor, joystick1, joystick2

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
		left = self.leftKalman.Update(self.joystick1.GetY())
		right = self.rightKalman.Update(self.joystick2.GetY())

		# Set the motors to the values
		leftDriveMotor.Set(left)
		rightDriveMotor.Set(right)

		# We return false so this is never removed from the scheduler
		return False

	def DriveForTime(self, timeToWait=0, speed=0.5):
		"""
		This will be able to be registered with the scheduler
		and stop driving after X amount of time.

		The reason we default time to 0 is just in case the 
		method is registered with the scheduler without any
		parameters.

		Keyword arguments:
		@time -- The time to do this is milliseconds
		"""
		if self.time == 0:
			self.time = time.time()

		currentTime = time.time()
		if (currentTime - self.time) >= timeToWait:
			self.time = 0
			leftDriveMotor.Disable()
			rightDriveMotor.Disable()
			return True
		else:
			self.time = currentTime
			leftDriveMotor.Set(speed)
			rightDriveMotor.Set(speed)
			return False




from scheduler import scheduler

drive = Drive()
scheduler.RegisterOperatorControlTask("Operator drive", drive.DriveTeleop)