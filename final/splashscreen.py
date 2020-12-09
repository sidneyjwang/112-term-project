#####################################
# splash screen
#####################################

from cmu_112_graphics import *

# from the 112 course website:
def rgbString(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

class splashscreen(Mode):
    def appStarted(mode):
        mode.mouseX, mode.mouseY = 0, 0
        mode.SSbackground = mode.loadImage('samplesandbackground.png')
        mode.center = mode.width / 2
        mode.titlePositionY = mode.height/4
        mode.textHeight = 20
        mode.sandboxTextY = mode.height/16*7
        mode.sandboxWidth = 80
        mode.sandboxColor = rgbString(0,0,0)
        mode.pictureTextY = mode.height/16*9
        mode.pictureWidth = 70
        mode.pictureColor = rgbString(0,0,0)
        mode.gameTextY = mode.height/16*11
        mode.gameWidth = 60
        mode.gameColor = rgbString(0,0,0)

    def mouseMoved(mode, event):
        mode.mouseX, mode.mouseY = event.x, event.y

    # check if a button was pressed
    def mousePressed(mode, event):
        if (mode.center-mode.sandboxWidth < mode.mouseX < mode.center+mode.sandboxWidth and
        mode.sandboxTextY-mode.textHeight < mode.mouseY < mode.sandboxTextY+mode.textHeight):
            # replace with sandbox mode
            mode.app.setActiveMode(mode.app.sandboxMode)
        elif (mode.center-mode.pictureWidth < mode.mouseX < mode.center+mode.pictureWidth and
        mode.pictureTextY-mode.textHeight < mode.mouseY < mode.pictureTextY+mode.textHeight):
            # replace with picture mode
            mode.app.setActiveMode(mode.app.pictureMode)
        elif (mode.center-mode.gameWidth < mode.mouseX < mode.center+mode.gameWidth and
        mode.gameTextY-mode.textHeight < mode.mouseY < mode.gameTextY+mode.textHeight):
            # replace with game mode
            mode.app.setActiveMode(mode.app.gameMode)

    # check if the mouse is hovering over text; if so, make it gray :)
    def timerFired(mode):
        if (mode.center-mode.sandboxWidth < mode.mouseX < mode.center+mode.sandboxWidth and
        mode.sandboxTextY-mode.textHeight < mode.mouseY < mode.sandboxTextY+mode.textHeight):
            mode.sandboxColor = rgbString(160,160,160)
            mode.pictureColor, mode.gameColor = rgbString(0,0,0), rgbString(0,0,0)
        elif (mode.center-mode.pictureWidth < mode.mouseX < mode.center+mode.pictureWidth and
        mode.pictureTextY-mode.textHeight < mode.mouseY < mode.pictureTextY+mode.textHeight):
            mode.pictureColor = rgbString(160,160,160)
            mode.sandboxColor, mode.gameColor = rgbString(0,0,0), rgbString(0,0,0)
        elif (mode.center-mode.gameWidth < mode.mouseX < mode.center+mode.gameWidth and
        mode.gameTextY-mode.textHeight < mode.mouseY < mode.gameTextY+mode.textHeight):
            mode.gameColor = rgbString(160,160,160)
            mode.sandboxColor, mode.pictureColor = rgbString(0,0,0), rgbString(0,0,0)
        else:
            mode.pictureColor = rgbString(0,0,0)
            mode.sandboxColor = rgbString(0,0,0)
            mode.gameColor = rgbString(0,0,0)

    # bring up the help page
    def keyPressed(mode, event):
        if event.key == 'Space':
            mode.app.setActiveMode(mode.app.helpMode)

    def redrawAll(mode, canvas):
        canvas.create_image(mode.width / 2, mode.height, 
                            image=ImageTk.PhotoImage(mode.SSbackground), anchor='s')
        canvas.create_text(mode.center, mode.titlePositionY, 
                            text='thisisntsand', font=("Avenir", 32, "bold"))
        canvas.create_text(mode.center, mode.sandboxTextY, text='sandbox  >',
                            font=("Avenir", 24), fill=mode.sandboxColor)
        canvas.create_text(mode.center, mode.pictureTextY, text='picture  >',
                            font=("Avenir", 24), fill=mode.pictureColor)
        canvas.create_text(mode.center, mode.gameTextY, text='game  >',
                            font=("Avenir", 24), fill=mode.gameColor)