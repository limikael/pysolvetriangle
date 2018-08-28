import math

#
# Algorithm from here: https://en.wikipedia.org/wiki/Solution_of_triangles
#

class Triangle:

	def __init__(self, sides=None, radians=None, degrees=None):
		self.__sides=Triangle.__fill_array(sides)

		if degrees is not None:
			degrees=Triangle.__fill_array(degrees)
			self.__angles=[
				math.radians(degrees[0]) if degrees[0] is not None else None,
				math.radians(degrees[1]) if degrees[1] is not None else None,
				math.radians(degrees[2]) if degrees[2] is not None else None,
			]

		else:
			self.__angles=Triangle.__fill_array(radians)

		self.__other=None
		self.__solve()

	def get_degrees(self):
		return [
			self.get_degree(0),
			self.get_degree(1),
			self.get_degree(2)
		]

	def get_degree(self, i):
		return math.degrees(self.__angles[i]) if self.__angles[i] is not None else None

	def get_sides(self):
		return self.__sides

	def get_side(self, i):
		return self.__sides[i]

	def get_radian(self, i):
		return self.__angles[i]

	def get_radians(self):
		return self.__angles

	def get_other(self):
		if self.__other is None:
			return self

		return self.__other

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

	def __solve(self):
		if self.__num_not_none(self.__sides)+self.__num_not_none(self.__angles)>3:
			raise Exception("Over constrained")

		#SSS - law of cosines
		if Triangle.__num_not_none(self.__sides)==3:
			for i in range(0,2):
				n=self.__sides[(i+1)%3]**2 + self.__sides[(i+2)%3]**2 - self.__sides[i]**2
				m=2*self.__sides[(i+1)%3]*self.__sides[(i+2)%3]
				self.__angles[i]=math.acos(float(n)/float(m))

			self.__compute_missing_angle()

		#SAS or SSA
		if (Triangle.__num_not_none(self.__sides)==2
				and Triangle.__num_not_none(self.__angles)>=1):

			# Included angle (SAS)
			if Triangle.__first_none(self.__sides)==Triangle.__first_not_none(self.__angles):
				c=Triangle.__first_none(self.__sides)
				a=(c+1)%3
				b=(c+2)%3

				self.__sides[c]=math.sqrt(self.__sides[a]**2 + self.__sides[b]**2
					-2*self.__sides[a]*self.__sides[b]*math.cos(self.__angles[c]))

				self.__angles[a]=math.acos((self.__sides[b]**2 +  self.__sides[c]**2 - self.__sides[a]**2)
					/(2*self.__sides[b]*self.__sides[c]))

				self.__compute_missing_angle()
				pass

			# Not the included angle (SSA)
			else:
				a=Triangle.__first_none(self.__sides)
				b=Triangle.__first_not_none(self.__angles)
				cands=[0,1,2]
				cands.remove(a)
				cands.remove(b)
				c=cands[0]

				term1=self.__sides[c]*math.cos(self.__angles[b])
				term2=math.sqrt(self.__sides[b]**2 - (self.__sides[c]*math.sin(self.__angles[b]))**2)
				self.__sides[a]=term1+term2

				o=[None,None,None]
				o[a]=term1-term2
				o[b]=self.__sides[b]
				o[c]=self.__sides[c]
				self.__other=Triangle(o)

				i=self.__first_none(self.__angles)
				n=self.__sides[(i+1)%3]**2 + self.__sides[(i+2)%3]**2 - self.__sides[i]**2
				m=2*self.__sides[(i+1)%3]*self.__sides[(i+2)%3]
				self.__angles[i]=math.acos(float(n)/float(m))
				self.__compute_missing_angle()

		#ASA - law of sines
		elif Triangle.__num_not_none(self.__angles)>=2:
			if Triangle.__num_not_none(self.__angles)==2:
				self.__compute_missing_angle()

			n=Triangle.__first_not_none(self.__sides)
			a=(n+1)%3
			b=(n+2)%3
			self.__sides[a]=self.__sides[n]*math.sin(self.__angles[a])/math.sin(self.__angles[n])
			self.__sides[b]=self.__sides[n]*math.sin(self.__angles[b])/math.sin(self.__angles[n])

		else:
			raise Exception("Too little info")

	def __compute_missing_angle(self):
		missing=Triangle.__first_none(self.__angles)
		self.__angles[missing]=math.pi-self.__angles[(missing+1)%3]-self.__angles[(missing+2)%3]

	@staticmethod
	def __fmt(num):
		if num is None:
			return "None"

		return "%.1f"%num

	def __repr__(self):
		d=self.get_degrees()
		return "Triangle[[%.1f, %.1f, %.1f] - d=[%.0f, %.0f, %.0f]]"%(
			self.__sides[0], self.__sides[1], self.__sides[2],
			d[0], d[1], d[2]
		)


if __name__=="__main__":
	print Triangle([10,10,10])
	print "other: ",Triangle([10,10,10]).get_other()
	print Triangle([None,10],degrees=[90,45])
	print Triangle([10,None,10],degrees=[None,90])
	print Triangle([1,2],degrees=[20])
	print "other: ",Triangle([1,2],degrees=[20]).get_other()