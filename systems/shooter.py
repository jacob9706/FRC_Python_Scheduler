from get_wpilib import wpilib

from robotmap import *

from utilities.pid import PID


class Shooter(object):

	SHOOTER_SCALE_FACTOR = 24800.0

	SHOOTER_POWER_SAVING_MODE = 0.4;
	SHOOTER_PYRIMID = 0.55;
	SHOOTER_INFIELD = 0.8;
	SHOOTER_3QUARTERS = 0.85;

	def __init__(self):
		"""
		Do things like create filters or initialize variables.
		"""
		shooterEncoder.scaleFactor = Shooter.SHOOTER_SCALE_FACTOR
		self.pidCalculator = PID(.1, 0, 0, shooterEncoder)
		self.pidCalculator.SetOutputRange(-1.0, 1.0)
		self.pidCalculator.Enable()

		self.enabled = True
		
		# Create and enable timer
		self.shootTimer = wpilib.Timer()
		self.shootTimer.Start()
		
		# These are for kicking timing
		self.startTime = 0.0
		self.timerStarted = False

	def ShooterTeleop(self):
		"""
		This is the method we will register as a task with the
		scheduler to be called in OperatorControl (ie. teleop)

		Convention is to name it "ClassNameTeleop" because when
		it is registered with the scheduler it uses that name
		to check if one is already registered if you tell it to.
		If it was just Teleop and we had a Teleop method from
		another class registered it would not schedule it.
		"""
		if self.enabled:
			# If Y is pressed
			if joystick1.GetRawButton(4):
				self.SetSpeed(Shooter.SHOOTER_POWER_SAVING_MODE)
			# If X is pressed
			if joystick1.GetRawButton(3):
				self.SetSpeed(Shooter.SHOOTER_INFIELD)
			# If B is pressed
			if joystick1.GetRawButton(2):
				self.SetSpeed(Shooter.SHOOTER_INFIELD)
			# If A is pressed
			if joystick1.GetRawButton(1):
				self.SetSpeed(Shooter.SHOOTER_3QUARTERS)
			if joystick1.GetRawButton(7):
				shooterMotor.Disable()
				self.SetSpeed(0.0)
				self.pidCalculator.Reset()

			self.ShooterContinuous()
		else:
			self.pidCalculator.Reset()
			tiltMotor.Disable()
			
	def ShooterContinuous(self):
		# Use calculated PID value
		output = self.pidCalculator.Get()
		# Set output of motor
		shooterMotor.Set(output)
#		print("Shooter Motor", shooterMotor.Get())

	def SetSpeed(self, speed):
		self.pidCalculator.SetSetpoint(speed)
		if not self.pidCalculator.IsEnabled():
			self.pidCalculator.Enable()
		return True
	
	def Shoot(self):
		if self.timerStarted is False:
			self.timerStarted = True
			self.startTime = self.shootTimer.Get()
			
		passedTime = self.shootTimer.Get() - self.startTime
		if passedtime < 0.2:
			hopperSolenoid.Set(True)
		elif passedTime < 0.25:
			hopperSolenoid.Set(False)
			self.timerStarted = False
			# Return false to end task if it was scheduled
			return True
		# We need to keep running
		return False
		
	def ShootAndLoad(self):
		if self.timerStarted is False:
			self.timerStarted = True
			self.shootTimer.Reset()
			self.shootTimer.Start()
			
		passedTime = self.shootTimer.Get()# - self.startTime
		print(passedTime)
		if passedTime < 0.2:
			shooterSolenoid.Set(True)
		elif passedTime < 0.25:
			shooterSolenoid.Set(False)
		elif passedTime < 0.85:
			hopperSolenoid.Set(True)
		else:
			# Return false to end task if it was scheduled
			hopperSolenoid.Set(False)
			self.timerStarted = False
			return True
		# We need to keep running
		return False
		

################### Register with scheduler ###################
from systems.scheduler import scheduler

shooter = Shooter()
scheduler.RegisterOperatorControlTask("Shooter Teleop", shooter.ShooterTeleop)
