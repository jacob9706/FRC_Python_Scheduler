from get_wpilib import wpilib
from utilities.kalman import Kalman

class SmoothEncoder(wpilib.Encoder):
	def __init__(self, port1, port2, reverseDirection=False, encoding_type=1):
		super(SmoothEncoder, self).__init__(port1, port2, reverseDirection, encoding_type)
		
		self.scaleFactor = 1.0
		self.kalmanFilter = Kalman()
		
	def SetKalman(self, q=0.001, r=0.1, p=1.0, x=0.0 , k=0.0):
		self.kalmanFilter.q = q
		self.kalmanFilter.r = r
		self.kalmanFilter.p = p
		self.kalmanFilter.x = x
		self.kalmanFilter.k = k
	
	def Get(self):
		value = super(SmoothEncoder, self).Get()
		value = self.kalmanFilter.Update(value)
		return value/self.scaleFactor
		
	def PIDGet(self):
		value = super(SmoothEncoder, self).PIDGet()
		value = self.kalmanFilter.Update(value)
		return value/self.scaleFactor
