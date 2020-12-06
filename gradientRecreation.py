###############################
# gradient selection for recreation mode
###############################

from cmu_112_graphics import *
import string

# takes in a rgbString and converts it to RGB
def rgbStringtoRGB(rgbString):
    red1 = convertHexDigitToBaseTen(rgbString[1])
    red2 = convertHexDigitToBaseTen(rgbString[2])
    green1 = convertHexDigitToBaseTen(rgbString[3])
    green2 = convertHexDigitToBaseTen(rgbString[4])
    blue1 = convertHexDigitToBaseTen(rgbString[5])
    blue2 = convertHexDigitToBaseTen(rgbString[6])
    print(red1,red2,green1,green2,blue1,blue2)
    return (red2 + 16*red1, green2 + 16*green1, blue2 + 16*blue1)

# helper function for rgbStringtoRGB    
def convertHexDigitToBaseTen(digit):
    if digit in string.digits:
        return int(digit)
    else:
        return string.ascii_lowercase.find(digit) + 10

def rgbString(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

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
        print(x,y)
        print(mode.app.sandColor)

    def mouseReleased(mode, event):
        mode.app.setActiveMode(mode.app.recreationMode)