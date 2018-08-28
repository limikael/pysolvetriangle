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

		self.other=None
		self.solve()

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

	def get_other(self):
		if self.other is None:
			return self

		return self.other

	def solve(self):
		if self.__num_not_none(self.sides)+self.__num_not_none(self.angles)>3:
			raise Exception("Over constrained")

		#SSS - law of cosines
		if Triangle.__num_not_none(self.sides)==3:
			for i in range(0,2):
				n=self.sides[(i+1)%3]**2 + self.sides[(i+2)%3]**2 - self.sides[i]**2
				m=2*self.sides[(i+1)%3]*self.sides[(i+2)%3]
				self.angles[i]=math.acos(float(n)/float(m))

			self.compute_missing_angle()

		#SAS or SSA
		if (Triangle.__num_not_none(self.sides)==2
				and Triangle.__num_not_none(self.angles)>=1):

			# Included angle (SAS)
			if Triangle.__first_none(self.sides)==Triangle.__first_not_none(self.angles):
				c=Triangle.__first_none(self.sides)
				a=(c+1)%3
				b=(c+2)%3

				self.sides[c]=math.sqrt(self.sides[a]**2 + self.sides[b]**2
					-2*self.sides[a]*self.sides[b]*math.cos(self.angles[c]))

				self.angles[a]=math.acos((self.sides[b]**2 +  self.sides[c]**2 - self.sides[a]**2)
					/(2*self.sides[b]*self.sides[c]))

				self.compute_missing_angle()
				pass

			# Not the included angle (SSA)
			else:
				a=Triangle.__first_none(self.sides)
				b=Triangle.__first_not_none(self.angles)
				cands=[0,1,2]
				cands.remove(a)
				cands.remove(b)
				c=cands[0]

				term1=self.sides[c]*math.cos(self.angles[b])
				term2=math.sqrt(self.sides[b]**2 - (self.sides[c]*math.sin(self.angles[b]))**2)
				self.sides[a]=term1+term2

				o=[None,None,None]
				o[a]=term1-term2
				o[b]=self.sides[b]
				o[c]=self.sides[c]
				self.other=Triangle(o)

				i=self.__first_none(self.angles)
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
		return "Triangle[%s - d=[%s,%s,%s]]"%(self.sides,d[0],d[1],d[2])

if __name__=="__main__":
	print Triangle([10,10,10])
	print "other: ",Triangle([10,10,10]).get_other()
	print Triangle([None,10],degrees=[90,45])
	print Triangle([10,None,10],degrees=[None,90])
	print Triangle([1,2],degrees=[20])
	print "other: ",Triangle([1,2],degrees=[20]).get_other()