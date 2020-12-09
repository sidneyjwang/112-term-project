###############################
# gradient selection for sandbox mode
###############################

from cmu_112_graphics import *
import string
import copy

# takes in a rgbString and converts it to RGB
def rgbStringtoRGB(rgbString):
    red1 = convertHexDigitToBaseTen(rgbString[1])
    red2 = convertHexDigitToBaseTen(rgbString[2])
    green1 = convertHexDigitToBaseTen(rgbString[3])
    green2 = convertHexDigitToBaseTen(rgbString[4])
    blue1 = convertHexDigitToBaseTen(rgbString[5])
    blue2 = convertHexDigitToBaseTen(rgbString[6])
    return (red2 + 16*red1, green2 + 16*green1, blue2 + 16*blue1)

# helper function for rgbStringtoRGB    
def convertHexDigitToBaseTen(digit):
    if digit in string.digits:
        return int(digit)
    else:
        return string.ascii_lowercase.find(digit) + 10

def rgbString(r, g, b):
    r = int(r)
    g = int(g)
    b = int(b)
    return f'#{r:02x}{g:02x}{b:02x}'

class gradient(Mode):
    def appStarted(mode):
        mode.Gbackground = mode.loadImage('gradient.png')

    def drawCurrentColors(mode, canvas):
        for i in range(len(mode.app.sandColor)):
            canvas.create_oval(mode.width - 60 + 15 * i, 10 + 15 * i, 
                                mode.width - 10 - 15 * i, 60 - 15 * i, width=0,
                            fill=rgbString(mode.app.sandColor[i][0], 
                            mode.app.sandColor[i][1], mode.app.sandColor[i][2]))
    
    def redrawAll(mode, canvas):
        canvas.create_image(mode.width/2, mode.height/2,  
                            image=ImageTk.PhotoImage(mode.Gbackground))
        mode.drawCurrentColors(canvas)
        

    def mousePressed(mode, event):
        x, y = event.x, event.y
        color = list(mode.Gbackground.getpixel((x,y)))
        if color == [255,255,255]:
            color = [254,254,254]
        # white is not allowed
        # reset the gradient
        if mode.app.gradientModeJustOpened:
            mode.app.sandColor = [color]
            mode.app.sandboxMode.currentSandColor = mode.app.sandColor[0]
            mode.app.gradientModeJustOpened = False
        # add an additional color
        else:
            if len(mode.app.sandColor) < 2:
                mode.app.sandColor.append(color)

    # return back to old screen once space is pressed
    def keyPressed(mode, event):
        if event.key == 'Space':
            mode.app.setActiveMode(mode.app.sandboxMode)
            mode.app.returnedToSandbox = True
            mode.app.sandboxMode.counter = 50
            mode.app.sandboxMode.currentSandColor = copy.deepcopy(mode.app.sandColor[0])
    
    def mouseReleased(mode, event):
        if len(mode.app.sandColor) > 1:
            mode.app.setActiveMode(mode.app.sandboxMode)
            mode.app.returnedToSandbox = True
            mode.app.sandboxMode.currentSandColor = copy.deepcopy(mode.app.sandColor[0])
