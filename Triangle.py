import math

#
# Algorithm from here: https://en.wikipedia.org/wiki/Solution_of_triangles
#

class Triangle:

	def __init__(self, sides=None, angles=None, degrees=None):
		self.sides=Triangle.__fill_array(sides)

		if degrees is not None:
			degrees=Triangle.__fill_array(degrees)
			self.angles=[
				math.radians(degrees[0]) if degrees[0] is not None else None,
				math.radians(degrees[1]) if degrees[1] is not None else None,
				math.radians(degrees[2]) if degrees[2] is not None else None,
			]

		else:
			self.angles=Triangle.__fill_array(angles)

	@staticmethod
	def __fill_array(a,fill_len=3):
		if a is None:
			a=[]

		while len(a)<fill_len:
			a.append(None)

		return a

	@staticmethod
	def __num_not_none(a):
		n=0

		for i in range(0,len(a)):
			if a[i] is not None:
				n+=1

		return n

	@staticmethod
	def __first_none(a):
		for i in range(0,len(a)):
			if a[i] is None:
				return i

		raise Exception("No missing value")

	@staticmethod
	def __first_not_none(a):
		for i in range(0,len(a)):
			if a[i] is not None:
				return i

		raise Exception("No value defined")

	def solve(self):
		#SSS - law of cosines
		if Triangle.__num_not_none(self.sides)==3:
			for i in range(0,2):
				n=self.sides[(i+1)%3]**2 + self.sides[(i+2)%3]**2 - self.sides[i]**2
				m=2*self.sides[(i+1)%3]*self.sides[(i+2)%3]
				self.angles[i]=math.acos(float(n)/float(m))

			self.compute_missing_angle()

		#ASA - law of sines
		elif Triangle.__num_not_none(self.angles)>=2:
			if Triangle.__num_not_none(self.angles)==2:
				self.compute_missing_angle()

			n=Triangle.__first_not_none(self.sides)
			a=(n+1)%3
			b=(n+2)%3
			self.sides[a]=self.sides[n]*math.sin(self.angles[a])/math.sin(self.angles[n])
			self.sides[b]=self.sides[n]*math.sin(self.angles[b])/math.sin(self.angles[n])

		else:
			raise Exception("Too little info")

	def compute_missing_angle(self):
		missing=Triangle.__first_none(self.angles)
		self.angles[missing]=math.pi-self.angles[(missing+1)%3]-self.angles[(missing+2)%3]

	def get_degrees(self):
		return [
			self.get_degree(0),
			self.get_degree(1),
			self.get_degree(2)
		]

	def get_degree(self, i):
		return math.degrees(self.angles[i]) if self.angles[i] is not None else None

	def __repr__(self):
		d=self.get_degrees()
		return "Triangle[%s - d=[%d,%d,%d]]"%(self.sides,d[0],d[1],d[2])

if __name__=="__main__":
	t=Triangle([10,10,10])
	t.solve()
	print t

#	t=Triangle([10],degrees=[90,45])
	t=Triangle([None,10],degrees=[90,45])
	t.solve()
	print t
