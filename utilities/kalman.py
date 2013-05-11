class Kalman(object):
	def __init__(self, q=0.001, r=0.1, p=1.0, x=0.0 , k=0.0):
		self.q = q
		self.r = r
		self.p = p
		self.x = x
		self.k = k

	def Update(self, measurement):
		self.k = (self.p + self.q) / (self.p + self.q + self.r);
		self.p = self.r * (self.p + self.q) / (self.r + self.p + self.q);

		result = self.x + (measurement - self.x) * self.k;

		self.x = result

		return result