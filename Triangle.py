import math

#
# Algorithm from here: https://en.wikipedia.org/wiki/Solution_of_triangles
#

class Triangle:

	def __init__(self, sides=None, angles=None, degrees=None):
		self.sides=self.fill_array(sides)

		if degrees is not None:
			degrees=self.fill_array(degrees)
			self.angles=[
				math.radians(degrees[0]) if degrees[0] is not None else None,
				math.radians(degrees[1]) if degrees[1] is not None else None,
				math.radians(degrees[2]) if degrees[2] is not None else None,
			]

		else:
			self.angles=self.fill_array(angles)

	def fill_array(self,a,fill_len=3):
		if a is None:
			a=[]

		while len(a)<fill_len:
			a.append(None)

		return a

	def num_defined_sides(self):
		n=0

		for i in range(0,3):
			if self.sides[i] is not None:
				n+=1

		return n

	def num_defined_angles(self):
		n=0

		for i in range(0,3):
			if self.angles[i] is not None:
				n+=1

		return n

	def solve(self):
		#SSS - law of cosines
		if self.num_defined_sides()==3:
			for i in range(0,2):
				n=self.sides[(i+1)%3]**2 + self.sides[(i+2)%3]**2 - self.sides[i]**2
				m=2*self.sides[(i+1)%3]*self.sides[(i+2)%3]
				self.angles[i]=math.acos(float(n)/float(m))

			self.compute_missing_angle()
			return

		#ASA - law of sines
		if self.num_defined_angles()>=2:
			if self.num_defined_angles()==2:
				self.compute_missing_angle()

			n=self.get_defined_side()
			a=(n+1)%3
			b=(n+2)%3
			self.sides[a]=self.sides[n]*math.sin(self.angles[a])/math.sin(self.angles[n])
			self.sides[b]=self.sides[n]*math.sin(self.angles[b])/math.sin(self.angles[n])
			return

		raise Exception("Too little info")

	def compute_missing_angle(self):
		missing=self.get_missing_angle()
		self.angles[missing]=math.pi-self.angles[(missing+1)%3]-self.angles[(missing+2)%3]

	def get_missing_angle(self):
		for i in range(0,3):
			if self.angles[i] is None:
				return i

		raise Exception("No missing angle")

	def get_defined_side(self):
		for i in range(0,3):
			if self.sides[i] is not None:
				return i

		raise Exception("No defined")

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
