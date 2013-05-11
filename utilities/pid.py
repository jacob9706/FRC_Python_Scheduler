from get_wpilib import wpilib

class PID(wpilib.PIDController):
	def __init__(self, Kp, Ki, Kd, source, period=0.05):
		super(PID, self).__init__(Kp, Ki, Kd, source, None, period=0.05)


	def _PIDController__calculate(self):
		"""
		* Read the input, calculate the output accordingly, and write to the output.
		* This should only be called by the Notifier indirectly through CallCalculate
		* and is created during initialization.
		"""    
        
		enabled = self.m_enabled
		pidInput = self.m_pidInput

		if enabled:

		    input = pidInput.PIDGet()

		    self.m_error = self.m_setpoint - input
		    if self.m_continuous:
		        
		        if math.fabs(self.m_error) > (self.m_maximumInput - self.m_minimumInput) / 2:
		            if self.m_error > 0:
		                self.m_error = self.m_error - self.m_maximumInput + self.m_minimumInput
		            else:
		                self.m_error = self.m_error + self.m_maximumInput - self.m_minimumInput

		    potentialIGain = (self.m_totalError + self.m_error) * self.m_I
		    
		    if potentialIGain < self.m_maximumOutput:
		        if potentialIGain > self.m_minimumOutput:
		            self.m_totalError += self.m_error
		        else:
		            self.m_totalError = self.m_minimumOutput / self.m_I
		    else:
		        self.m_totalError = self.m_maximumOutput / self.m_I

		    self.m_result = self.m_P * self.m_error + self.m_I * self.m_totalError + self.m_D * (self.m_error - self.m_prevError)
		    self.m_prevError = self.m_error

		    if self.m_result > self.m_maximumOutput:
		        self.m_result = self.m_maximumOutput
		    elif self.m_result < self.m_minimumOutput:
		        self.m_result = self.m_minimumOutput

		    pidOutput = self.m_pidOutput
		    result = self.m_result