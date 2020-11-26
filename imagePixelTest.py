# this is an image test
# this project uses cmu-112-graphics, which was taken from
# https://www.cs.cmu.edu/~112/

# implements Bresenham's Line Drawing Algorithm
# I used the following as a resource: 
# https://inst.eecs.berkeley.edu/~cs150/fa10/Lab/CP3/LineDrawing.pdf

from cmu_112_graphics import *

def appStarted(app):
    app.mouseMovedDelay = 1
    app.mouseX, app.mouseY = 0, 0
    app.oldMouseX, app.oldMouseY = 0, 0
    app.background = app.loadImage('blacktestbackground.png')

def mousePressed(app, event):
    app.mouseX, app.mouseY = event.x, event.y

def mouseDragged(app, event):
    app.oldMouseX, app.oldMouseY = app.mouseX, app.mouseY
    app.mouseX, app.mouseY = event.x, event.y
    print('mouseX, mouseY:', app.mouseX, app.mouseY)
    linePoints = getLinePoints(app.oldMouseX, app.oldMouseY, app.mouseX, app.mouseY)
    print('last point:', linePoints[-1])
    for x, y in linePoints:
        for horizontal in range(x-1, x+2):
            for vertical in range(y-1, y+2):
                app.background.putpixel((horizontal,vertical),(255,255,255))


def getLinePoints(x0,y0,x1,y1):
    didSwitch = False
    # if the line is vertical:
    if y1 > y0 and x0 == x1:
        return [(x0, y0+i) for i in range(y1-y0+1)]
    elif y0 > y1 and x0 == x1:
        return [(x0, y1+i) for i in range(y0-y1+1)]
    # check to see if the slope is greater than 1:
    if abs(y1-y0) > abs(x1-x0):
        print('thishappened')
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        didSwitch = True
    # if the line is being drawn from right --> left
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    slope = (y1-y0)/(x1-x0)
    dError = abs(slope)
    yStep = 1
    if y0 > y1:
        yStep = -1
    error = 0
    y = y0
    result = []
    for x in range(x0,x1+1):
        if didSwitch:
            result.append((y,x))
        else:
            result.append((x,y))
        error += dError
        if error >= 0.5:
            y += yStep
            error -= 1
    return result

def redrawAll(app, canvas):
    canvas.create_image(app.width/2, app.height/2,  
                        image=ImageTk.PhotoImage(app.background))

runApp(width=600, height=400)