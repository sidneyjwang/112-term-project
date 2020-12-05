##################################
# picture mode page
##################################

from cmu_112_graphics import *

# from the 112 course website:
def rgbString(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

class picture(Mode):
    def appStarted(mode):
        mode.mouseX, mode.mouseY = 0, 0
        mode.pictureBackground = mode.loadImage('samplesandbackground.png')
        mode.textHeight = 15
        mode.recreateWidth = 50
        mode.animateWidth = 50
        mode.recreatePos = (mode.width / 4, mode.height / 16 * 8)
        mode.animatePos = (mode.width / 4 * 3, mode.height / 16 * 8)
        mode.recreateColor = rgbString(0,0,0)
        mode.animateColor = rgbString(0,0,0)
        mode.app.imageName = mode.getUserInput('Please input name of file:')
        print(mode.app.imageName)

    def mouseMoved(mode, event):
        mode.mouseX, mode.mouseY = event.x, event.y

    def mousePressed(mode, event):
        if (mode.recreatePos[0]-mode.recreateWidth <= mode.mouseX <= mode.recreatePos[0]+mode.recreateWidth and
        mode.recreatePos[1]-mode.textHeight <= mode.mouseY <= mode.recreatePos[1]+mode.textHeight):
            print('recreate!')
        elif (mode.animatePos[0]-mode.animateWidth <= mode.mouseX <= mode.animatePos[0]+mode.animateWidth and
        mode.animatePos[1]-mode.textHeight <= mode.mouseY <= mode.animatePos[1]+mode.textHeight):
            print('animate!')
            mode.app.setActiveMode(mode.app.animationMode)

    def timerFired(mode):
        if (mode.recreatePos[0]-mode.recreateWidth <= mode.mouseX <= mode.recreatePos[0]+mode.recreateWidth and
        mode.recreatePos[1]-mode.textHeight <= mode.mouseY <= mode.recreatePos[1]+mode.textHeight):
            mode.recreateColor = rgbString(160,160,160)
            mode.animateColor = rgbString(0,0,0)
        elif (mode.animatePos[0]-mode.animateWidth <= mode.mouseX <= mode.animatePos[0]+mode.animateWidth and
        mode.animatePos[1]-mode.textHeight <= mode.mouseY <= mode.animatePos[1]+mode.textHeight):
            mode.animateColor = rgbString(160,160,160)
            mode.recreateColor = rgbString(0,0,0)
        else:
            mode.animateColor = rgbString(0,0,0)
            mode.recreateColor = rgbString(0,0,0)

    def keyPressed(mode, event):
        if event.key == 'Enter':
            mode.app.setActiveMode(mode.app.splashscreenMode)

    def redrawAll(mode, canvas):
        canvas.create_text(mode.width / 2, mode.height / 16 * 3, text='picture mode', 
                            font=('Avenir', 30, 'bold'))
        canvas.create_text(mode.recreatePos[0], mode.recreatePos[1], text='recreate', 
                            font=('Avenir', 24), fill=mode.recreateColor)
        canvas.create_text(mode.animatePos[0], mode.animatePos[1], text='animate', 
                            font=('Avenir', 24), fill=mode.animateColor)
        canvas.create_image(mode.width/2, mode.height, anchor='s', 
                                image=ImageTk.PhotoImage(mode.pictureBackground))