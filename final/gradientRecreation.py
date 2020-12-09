###############################
# gradient selection for recreation mode
###############################

from cmu_112_graphics import *
import string

class gradientRecreation(Mode):
    def appStarted(mode):
        mode.Gbackground = mode.loadImage('gradient.png')

    def redrawAll(mode, canvas):
        canvas.create_image(mode.width/2, mode.height/2,  
                            image=ImageTk.PhotoImage(mode.Gbackground))

    def mousePressed(mode, event):
        x, y = event.x, event.y
        color = mode.Gbackground.getpixel((x,y))
        if color == (255,255,255):
            color = (254,254,254)
        mode.app.sandColor = color

    def mouseReleased(mode, event):
        mode.app.setActiveMode(mode.app.recreationMode)