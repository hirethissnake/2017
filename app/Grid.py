"""Make weighted grid."""
from appJar import gui
from random import randint
import colorsys

class Grid:

	def __init__(self, size):
		"""Initialization code. Set grid size and create blank grid
		of size x size shape."""
		self.size = size # set grid size
		self.grid = [[0 for i in range(size)] for j in range(size)] # generate a grid of size x size
	
	
	def getSize(self):
		"""Return grid size"""
	
		
	def randomizeWeights(self, min, max):
		"""Fill grid with random values between min and max."""
		self.grid = [[randint(min, max) for i in range(self.size)] for j in range(self.size)] # fill grid with numbers between min and max
	
	
	def weightCell(self, row, col, modifier):
		"""Multiple cell by modifier value"""
		#TODO
			#Modify grid cell
			
	
	def setCell(self, row, col, value):
		"""Set cell to value"""
		#TODO
			#Set grid cell
			
	
	def getCell(self, row, col):
		"""Return cell value"""
		#TODO
			#Return cell value
	
	
	def showColours(self):
		"""Use colours to visualize each step of the algorithm,
		to see how different cells are weighted differently."""
		app = gui('Login Window', '400x400')
		app.setBg('white')
		app.setTitle('SneakySnake Visualiser')

		for i in range(self.size):
			for k in range(self.size):
				gridValue = self.grid[i][k]
				
				# interpolate square value from gridValue into HSV value between red and green, convert to RGB, convert to hex
				hex = '#%02x%02x%02x' % tuple(i * 255 for i in colorsys.hls_to_rgb((gridValue * 1.2) / float(360), 0.6, 0.8))
				if gridValue == 0: # color perfect non-valid entries black
					hex = '#000000'
				if gridValue == 100: # color perfect full-valid entries blue
					hex = '#2196F3'
				if gridValue > 100 or gridValue < 0: # color invalid entries grey
					hex = '#616161'
				title = str(i) + "," + str(k)
				app.addLabel(title, '', i, k)
				app.setLabelBg(title, hex)

		app.go()
		
		
	def showNumbers(self):
		"""Use numbers to visualize each step of the algorithm,
		to see how different cells are weighted differently."""
		#TODO
			#Show visualization
		
		
	"""def addBoundary(self, value):
		#Weight fully negative the walls of the grid. This assumes our grid
		#size includes the wall cells.
		for i in range(self.size):
			self.grid[0][i] = value
			self.grid[-1][i] = value
			self.grid[i][0] = value
			self.grid[i][-1] = value""" #I don't think we need a boundary, unnecessary storage, can simply check bounds and set weight to 0