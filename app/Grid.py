from appJar import gui
from random import randint
import colorsys

class Grid:

	def __init__(self, size):
	
		self.size = size # set grid size
		self.grid = [[0 for i in range(size)] for j in range(size)] # generate a grid of size x size
		
		
	def randomize(self, min, max):
	
		self.grid = [[randint(min, max) for i in range(self.size)] for j in range(self.size)] # fill grid with numbers between min and max
	
	
	def show(self):
	
		app = gui('Login Window', '400x400')
		app.setBg('white')
		app.setTitle('SneakySnake Visualiser')

		for i in range(self.size):
			for k in range(self.size):
				gridValue = self.grid[i][k]
				
				# interpolate square value from gridValue into HSV value between red and green, convert to RGB, convert to hex
				hex = '#%02x%02x%02x' % tuple(i * 255 for i in colorsys.hls_to_rgb((gridValue * 1.2) / float(360), 0.6, 0.8))
				
				title = str(i) + "," + str(k)
				app.addLabel(title, '', i, k)
				app.setLabelBg(title, hex)

		app.go()
		
		
	def addBoundary(self, value):
	
		for i in range(self.size):
			self.grid[0][i] = value
			self.grid[-1][i] = value
			self.grid[i][0] = value
			self.grid[i][-1] = value