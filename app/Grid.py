"""Make weighted grid."""
from random import randint
import colorsys
# from appJar import gui

class Grid:
    """Store board location weights in 2D array."""

    def __init__(self, size):
        """Initialization code. Set grid size and create blank grid of size x size shape."""
        # pylint: disable=W0612
        self.size = size # set grid size
        # generate a grid of size x size
        self.grid = [[0 for i in range(size)] for j in range(size)]


    def getSize(self):
        """Return grid size"""


    def randomizeWeights(self, minWeight, maxWeight):
        """Fill grid with random values between min and max."""
        # pylint: disable=W0612
        # fill grid with numbers between min and max
        self.grid = [[randint(min, max) for i in range(self.size)]
                    for j in range(self.size)]


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
        # app = gui('Login Window', '400x400')
        # app.setBg('white')
        # app.setTitle('SneakySnake Visualiser')

        for i in range(self.size):
            for k in range(self.size):
                gridValue = self.grid[i][k]

                # interpolate square value from gridValue into HSV value
                # between red and green, convert to RGB, convert to hex
                hexCode = '#%02x%02x%02x' % tuple(i * 255 for i in
                            colorsys.hls_to_rgb((gridValue * 1.2) /
                            float(360), 0.6, 0.8))
                if gridValue == 0: # color perfect non-valid entries black
                    hexCode = '#000000'
                if gridValue == 100: # color perfect full-valid entries blue
                    hexCode = '#2196F3'
                if gridValue > 100 or gridValue < 0: # color invalid entries grey
                    hexCode = '#616161'
                title = str(i) + "," + str(k)
                # app.addLabel(title, '', i, k)
                # app.setLabelBg(title, hexCode)

        # app.go()


    def showNumbers(self):
        """Use numbers to visualize each step of the algorithm,
        to see how different cells are weighted differently."""
        #TODO
            #Show visualization
