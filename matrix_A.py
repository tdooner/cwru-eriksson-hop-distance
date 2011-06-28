#!/usr/bin/python
#
#    Implements some features of the matrix A, a matrix
#     that is m x m ( where m is the number of vantage points )
#
#  To use:
#	from matrix_A import matrix_A
#	m = matrix_A("/path/to/matrixFile.dhr")
#		where "matrixFile.dhr"
#
from array import array
from numpy import linalg as LA

class matrix_A:
	hosts = [] 	# Hashtable of hosts    	   id => ip address
	hosts_hops = [] # Hashtable of hashtable of hops   id => id => hops
			# (note: these IDs will correspond and
			#   hosts_hops[n][n] == "1.0")
	def __init__(self, filename):
		f = open(filename, "r")
		# Up to the delimiter
		for i in f:
			i = i.strip()   # (you never know...)
			if i == "$$":
				break
			self.hosts.append(i)
		# After the delimiter
		for i in f:
			items = i.strip().split(" ")
			tmp_row = []
			tmp_row_array = array("I")
			for j in items:
				tmp_row.append(float(j))
			self.hosts_hops.append(tmp_row)
		
	def energy_ratio(self, d):
		try:
			total = 0
			for (i, j) in enumerate(self.eigenvectors):
				if (i >= d):
					break
				total += j
			return total/self.eigenvectors.sum()
		except NameError:
			print "Error! Eigenvectors not defined!"
		except:
			print "An error occurred!"

	def calculate_dimension(self):
		d = 0;
		self.eigenvectors = LA.eig(self.hosts_hops)[0]
		print self.eigenvectors
		for i in range(0, 1000):
			print self.energy_ratio(i)
			if self.energy_ratio(i) > 0.9:
				self.dimension = i
				return

m = matrix_A("mSubsetMatrix.dhr")
m.calculate_dimension()
print m.dimension
