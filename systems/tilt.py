from get_wpilib import wpilib

from robotmap import *

from utilities.pid import PID


class Tilt(object):

	TILT_FRISBEE_LOAD = -20; # Prod 0
	TILT_MID_COURT = -675; # Prod -495 |  21 deg -589
	TILT_PYRIMID_SIDE_PRACTICE = -678; # Prod(?)
	TILT_3QUARTS_COURT = -614; # Prod(-472) | 17-1/2 deg -472 at 85%

	def __init__(self):
		"""
		Do things like create filters or initialize variables.
		"""

		self.pidCalculator = PID(.009, 0, 0, tiltEncoder)
		self.pidCalculator.Enable()

		self.enabled = True

	def TiltTeleop(self):
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
				self.TiltToValue(Tilt.TILT_FRISBEE_LOAD)
			# If X is pressed
			if joystick1.GetRawButton(3):
				self.TiltToValue(Tilt.TILT_MID_COURT)
			# If B is pressed
			if joystick1.GetRawButton(2):
				self.TiltToValue(Tilt.TILT_PYRIMID_SIDE_PRACTICE)
			# If A is pressed
			if joystick1.GetRawButton(1):
				self.TiltToValue(Tilt.TILT_3QUARTS_COURT)
			self.TiltContinuous()
		else:
			self.pidCalculator.Reset()
			tiltMotor.Disable()
			
	def TiltContinuous(self):
		# Use calculated PID value
		output = self.pidCalculator.Get()
		# Safety Checks
		if (tiltZeroSwitch.Get() and output > 0) or (tiltSeventySwitch.Get() and output < 0):
			tiltMotor.Disable()
			self.tiltToValue(self.pidCalculator.GetSetpoint())
			self.pidCalculator.Reset()
		else:
			# Set output of motor
			tiltMotor.Set(output)
		#print("Tilt Motor", tiltMotor.Get())

	def TiltToValue(self, value):
		self.pidCalculator.SetSetpoint(value)
		if not self.pidCalculator.IsEnabled():
			self.pidCalculator.Enable()
		return True
	
	def TiltCalibrate(self):
		if not self.pidCalculator.IsEnabled():
			self.pidCalculator.Enable()
			
		if not tiltZeroSwitch.Get():
			current = self.pidCalculator.GetSetpoint()
			self.pidCalculator.SetSetpoint(current + 10)
			return False
		else:
			self.pidCalculator.SetSetpoint(0)
			tiltEncoder.Reset()
			return True

################### Register with scheduler ###################
from systems.scheduler import scheduler

tilt = Tilt()
scheduler.RegisterOperatorControlTask("Shooter Teleop", tilt.TiltTeleop)
