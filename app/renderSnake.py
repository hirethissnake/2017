from appJar import gui

# function called by pressing the buttons
def press(btn):
    if btn == "Cancel":
        app.stop()
    if btn == 'Submit':
        print 'User:', app.getEntry('user'), 'Pass:', app.getEntry('pass')
    else:
        app.infoBox('Help', 'Nah dawg, I can\'t help you.')

# app = gui('Login Window', '400x200')
app.setBg('white')
app.setFont(14, font='Segoe UI')
app.setTitle('SneakySnake Visualiser')

# app.startLabelFrame('Login Details')
# app.addLabel("user", "Username:", 0, 5)              # Row 0,Column 0
# app.addEntry("user", 0, 1)                           # Row 0,Column 1
# app.addLabel("pass", "Password:", 1, 0)              # Row 1,Column 0
# app.addSecretEntry("pass", 1, 1)                     # Row 1,Column 1
# app.addButtons(["Submit", "Cancel"], press, 2, 0, 2) # Row 2,Column 0,Span 2

# app.setEntryFocus("user")
# app.stopLabelFrame()

for i in range(10):
	for k in range(10):
		title = str(i) + "," + str(k)
		app.addLabel(title, ' ', i, k)
		app.setLabelBg(title, 'yellow')


app.go()
