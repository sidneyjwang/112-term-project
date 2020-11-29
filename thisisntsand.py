#####################################
# this is the main file- run this!
#####################################

# this project uses cmu-112-graphics, which was taken from
# https://www.cs.cmu.edu/~112/

from sandbox import *
from splashscreen import *

class thisIsntSand(ModalApp):
    def appStarted(app):
        app.splashscreenMode = splashscreen()
        app.sandboxMode = sandbox()
        app.setActiveMode(app.splashscreenMode)
        app.timerDelay = 5

thisIsntSand(width=600, height=400)