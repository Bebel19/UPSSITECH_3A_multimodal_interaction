#plate.py
import numpy as np
import math

nbItemsMax = 11


				

class Plate:
	
	def __init__(self,nbItemsMax):
		
		l = math.ceil(math.sqrt(nbItemsMax))
		self.plate = np.zeros((l,l))
		
	def add(name):
		for i in range(l):
			for j in range(l):
				if plate[i][j] != 0:
					plate[i][j] = name
					break
	def remove(name):
		for i in range(l):
			for j in range(l):
				if plate[i][j] != name:
					plate[i][j] = 0
					break
					
plate = Plate(nbItemsMax)
print(plate.plate)

