#####################################
# this is the main file- run this!
#####################################

# this project uses cmu-112-graphics, which was taken from
# https://www.cs.cmu.edu/~112/

import random
from sandbox import *
from splashscreen import *
from gradientPicker import *
from gamemode import *
from helpscreen import *
from picture import *

class thisIsntSand(ModalApp):
    def appStarted(app):
        app.splashscreenMode = splashscreen()
        app.sandboxMode = sandbox()
        app.gradientMode = gradient()
        app.gameMode = game()
        app.helpMode = helpScreen()
        app.pictureMode = picture()
        app.setActiveMode(app.splashscreenMode)
        app.timerDelay = 10 # change this to 10
        app.sandColor = (random.randint(1,254), random.randint(1,254), random.randint(1,254))

thisIsntSand(width=600, height=400)