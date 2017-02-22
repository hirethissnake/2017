from appJar import gui
import random
import colorsys

app = gui('Login Window', '400x400')
app.setBg('white')
app.setTitle('SneakySnake Visualiser')

# map is an NxN matrix of random values from 0 - 100
N = 20 # size of grid
map_gradient = [[int(random.random()*100) for i in range(N)] for j in range(N)] # generate grid of random numbers from 0-100
for i in range(N):
	# add walls
	map_gradient[0][i] = 0
	map_gradient[-1][i] = 0
	map_gradient[i][0] = 0
	map_gradient[i][-1] = 0

for i in range(len(map_gradient)):
	for k in range(len(map_gradient)):
		l = map_gradient[i][k]
		title = str(i) + "," + str(k)
		
		# interpolate square value from l into HSV value between red and green, convert to RGB, convert to hex
		hex = '#%02x%02x%02x' % tuple(i * 255 for i in colorsys.hls_to_rgb((l * 1.2) / float(360), 0.6, 0.8))
	
		app.addLabel(title, '', i, k)
		app.setLabelBg(title, hex)

app.go()
