#####################################
# ~welcome to thisisntsand~
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
from pictureAnimation import *
from recreation import *
from gradientRecreation import *

class thisIsntSand(ModalApp):
    def appStarted(app):
        app.splashscreenMode = splashscreen()
        app.sandboxMode = sandbox()
        app.gradientMode = gradient()
        app.gameMode = game()
        app.helpMode = helpScreen()
        app.pictureMode = picture()
        app.animationMode = animationMode()
        app.recreationMode = recreationMode()
        app.recreationGradientMode = gradientRecreation()
        app.setActiveMode(app.splashscreenMode) # begin on the splash screen
        app.timerDelay = 10 # change this to 10
        app.sandColor = [[random.randint(1,254), random.randint(1,254), random.randint(1,254)]]
        app.gradientModeJustOpened = False
        app.returnedToSandbox = False
        app.imageName = '' # this will be changed later if the user opens picture mode

thisIsntSand(width=600, height=400)